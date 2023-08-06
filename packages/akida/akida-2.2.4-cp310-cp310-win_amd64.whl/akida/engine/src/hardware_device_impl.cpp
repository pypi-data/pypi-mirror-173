#include "engine/hardware_device_impl.h"

#include <algorithm>
#include <cassert>
#include <cstdint>
#include <cstring>
#include <memory>
#include <tuple>

#include "akida/dense.h"
#include "akida/hw_version.h"
#include "akida/input_conversion.h"
#include "akida/np.h"
#include "akida/program_memory_info.h"
#include "akida/shape.h"
#include "engine/dma.h"
#include "engine/dma_config_ops.h"
#include "engine/dma_desc_ops.h"
#include "engine/dma_engine.h"
#include "engine/external_mem_mgr.h"
#include "engine/pipeline_state.h"
#include "infra/int_ops.h"
#include "infra/registers_common.h"
#include "infra/system.h"

#include "dma_desc_format.h"
#include "dma_engine_ops.h"
#include "dma_events_ops.h"
#include "dma_image_ops.h"
#include "epg_ops.h"
#include "mesh.h"
#include "program_play.h"
#include "registers_dma_engine.h"
#include "registers_top_level.h"
#include "reset_nps.h"

namespace akida {

static void toggle_multi_pass(HardwareDeviceImpl* device,
                              bool enable_multi_pass);

// Get hardware version from driver
static HwVersion get_version(const HardwareDriver& driver) {
  HwVersion version{0, 0, 0, 0};
  // Try first to read IP revision from device
  const auto top_level_reg_offset = driver.top_level_reg();
  auto reg = driver.read32(top_level_reg_offset + REG_IP_VERSION);
  auto vendor_id = static_cast<uint8_t>(get_field(reg, VENDOR_ID));
  if (reg != 0) {
    auto minor_rev = static_cast<uint8_t>(get_field(reg, MINOR_REV));
    auto major_rev = static_cast<uint8_t>(get_field(reg, MAJOR_REV));
    auto prod_id = static_cast<uint8_t>(get_field(reg, PROD_ID));
    version = {vendor_id, prod_id, major_rev, minor_rev};
  } else {
    // Legacy device: rely instead on the information provided by the driver
    auto driver_desc = driver.desc();
    if (strstr(driver_desc, "NSoC_v2") != nullptr) {
      version = NSoC_v2;

    } else if (strstr(driver_desc, "NSoC_v1") != nullptr) {
      version = NSoC_v1;
    }
  }
  return version;
}

static void alloc_dma_descriptors(HardwareDriver* driver, dma::Engine* dma,
                                  MemoryMgr* mem_mgr,
                                  uint32_t num_descriptors) {
  assert(num_descriptors <= dma::kMaxNbDescriptors);
  // if number of decriptor has changed or memory has not been allocated, set
  // number of containers and allocate descriptors buffer
  if (num_descriptors != dma->num_descriptors ||
      dma->descriptor_base_addr == 0) {
    if (dma->descriptor_base_addr) {
      mem_mgr->free(dma->descriptor_base_addr);
    }
    // allocate buffer to contain descriptors. Memory type is system:
    // this type will not be freed at unprogram, so descriptors will be
    // available as long as the device is available.
    dma->descriptor_base_addr =
        mem_mgr->alloc(num_descriptors * dma->descriptor_bytes_size);
    dma->num_descriptors = num_descriptors;
  }
  dma::configure_descriptors_buffer(driver, *dma);
}

static void free_dma_descriptors(dma::Engine* dma, MemoryMgr* mem_mgr) {
  if (dma->descriptor_base_addr) {
    mem_mgr->free(dma->descriptor_base_addr);
    // Currently we have to set to 0 to avoid double free
    dma->descriptor_base_addr = 0;
  }
}

HardwareDeviceImpl::HardwareDeviceImpl(HardwareDriver* driver)
    : driver_(driver),
      version_(get_version(*driver_)),
      mesh_(nullptr),
      dma_config_{dma::Engine(dma_config_reg_base(driver_->top_level_reg()),
                              dma::config::DESC_BYTE_SIZE)},
      dma_event_{dma::Engine(dma_event_reg_base(driver_->top_level_reg()),
                             dma::event::DESC_BYTE_SIZE)},
      dma_hrc_{dma::Engine(dma_hrc_reg_base(driver_->top_level_reg()),
                           dma::hrc::DESC_BYTE_SIZE)},
      mem_mgr_(driver->scratch_memory(), driver->scratch_size()),
      current_program_(nullptr, 0),
      current_program_learn_en_(false),
      external_mem_(&mem_mgr_, driver) {
  if (version_ == akida::NSoC_v1) {
    panic(
        "NSoC_v1 is not supported on this version. Please install akida 2.0.5 "
        "instead.");
  }
  init();
}

HardwareDeviceImpl::~HardwareDeviceImpl() {
  free_dma_descriptors(&dma_config_.engine, &mem_mgr_);
  free_dma_descriptors(&dma_event_.engine, &mem_mgr_);
  free_dma_descriptors(&dma_hrc_.engine, &mem_mgr_);
}

HwVersion HardwareDeviceImpl::version() const { return version_; }

void HardwareDeviceImpl::dma_config_write(const dma::w32* buffer,
                                          size_t buf_size) {
  // allocate buffer length
  auto input_addr = external_mem_.reserve(buffer, buf_size * sizeof(dma::w32));
  constexpr uint32_t output_addr = 0;  // not used for write
  // format descriptor
  auto descriptor =
      dma::format_config_desc(dma::kDescConfigDirectionWrite, input_addr,
                              output_addr, static_cast<uint32_t>(buf_size));
  assert(descriptor.size() == dma::config::DESC_LEN);

  // write buffer in DDR
  external_mem_.commit(buffer, buf_size * sizeof(dma::w32));

  // tell DMA engine to process descriptor
  dma::process(driver_, dma_config_, descriptor);
  // now that input has been processed, it can be freed
  external_mem_.release(buffer);
}

void HardwareDeviceImpl::dma_config_read(dma::w32* buffer,
                                         const struct np::Ident& np,
                                         dma::Target target,
                                         uint16_t addr_target_word,
                                         uint32_t nb_words) {
  assert(dma_config_.engine.descriptor_base_addr != 0);
  if (dma::config_block_size_needs_xl(static_cast<uint32_t>(nb_words))) {
    panic("Unsupported buffer size in config read");
  }

  // format header
  auto header =
      dma::format_config_header(np, target, nb_words, addr_target_word);
  uint32_t header_size = static_cast<uint32_t>(header.size());

  // Allocate input and output area
  auto input_addr = mem_mgr_.alloc(header_size * sizeof(dma::w32));
  // Allocation should include header size
  auto output_addr = mem_mgr_.alloc(nb_words * sizeof(dma::w32) +
                                    dma::kConfigReadPacketOffset);
  // format descriptor
  auto descriptor = dma::format_config_desc(
      dma::kDescConfigDirectionRead, input_addr, output_addr, header_size);
  assert(descriptor.size() == dma::config::DESC_LEN);

  // write header in DDR
  driver_->write(input_addr, header.data(), header.size() * sizeof(dma::w32));

  // tell DMA engine to process descriptor
  dma::process(driver_, dma_config_, descriptor);

  // fetch read header in DDR
  dma::wbuffer read_hdr(dma::kConfigReadPacketHdrSz);
  driver_->read(output_addr, read_hdr.data(),
                dma::kConfigReadPacketHdrSz * sizeof(dma::w32));

  // set packet size (nb of 32b words) and address/offset data
  uint32_t packetsize = dma::parse_config_read_size(read_hdr);
  uint32_t read_offset_addr = output_addr + dma::kConfigReadPacketOffset;

  if (nb_words == 0 || packetsize != nb_words) {
    panic("error on dma config read: invalid packet size (%d), expected %d.",
          packetsize, nb_words);
  }

  driver_->read(read_offset_addr, buffer, nb_words * sizeof(dma::w32));
  // now that input and outputs have been processed, it can be freed
  mem_mgr_.free(output_addr);
  mem_mgr_.free(input_addr);
}

void HardwareDeviceImpl::dma_start_config_multipass(dma::addr conf_base_address,
                                                    uint32_t num_descs,
                                                    uint32_t num_passes,
                                                    uint32_t num_extra_descs) {
  dma::start_config_multi_pass(driver_, dma_config_, conf_base_address,
                               num_descs, num_passes, num_extra_descs);
}

std::vector<TensorUniquePtr> HardwareDeviceImpl::fit(
    const std::vector<TensorConstPtr>& inputs,
    const std::vector<int32_t>& input_labels) {
  // Check the device had been programmed
  if (!current_program_.first) {
    panic("Cannot fit without a program");
  }
  if (!current_program_learn_en_)
    panic("Learn must be enabled to call the fit method.");

  return forward_loop(inputs, &input_labels);
}

std::vector<TensorUniquePtr> HardwareDeviceImpl::forward(
    const std::vector<TensorConstPtr>& inputs) {
  // Check the device had been programmed
  if (!current_program_.first) {
    panic("Cannot forward without a program");
  }
  if (current_program_learn_en_)
    panic("Learn must be disabled to call the forward method.");

  return forward_loop(inputs, nullptr);
}

const dma::Inputs& HardwareDeviceImpl::select_dma_engine(bool dense_inputs) {
  // Only enable the input DMA used by the current network:
  // HRC DMA if 1st layer is InputConvolutional, Event DMA otherwise
  dma::toggle_engine(driver_, dma_hrc_.engine.reg_base_addr, dense_inputs);
  dma::toggle_engine(driver_, dma_event_.engine.reg_base_addr, !dense_inputs);

  return dense_inputs ? dma_hrc_ : dma_event_;
}

void HardwareDeviceImpl::reset_dma_engines() {
  dma::reset(driver_, dma_config_.engine);
  dma::reset(driver_, dma_event_.engine);
  dma::reset(driver_, dma_hrc_.engine);
}

void HardwareDeviceImpl::pipeline(bool enabled) {
  dma::toggle_pipeline(driver_, dma_event_, enabled);
  dma::toggle_pipeline(driver_, dma_hrc_, enabled);
}

void HardwareDeviceImpl::toggle_clock_counter(bool enable) {
  dma::toggle_buffer_timer(driver_, dma_event_, enable);
  dma::toggle_buffer_timer(driver_, dma_hrc_, enable);
}

uint32_t HardwareDeviceImpl::read_clock_counter() {
  // read clock from HRC DMA or read from events DMA
  auto hrc_count_number = dma::read_buffer_timer(driver_, dma_hrc_);
  auto event_count_number = dma::read_buffer_timer(driver_, dma_event_);
  return std::max(hrc_count_number, event_count_number);
}

bool HardwareDeviceImpl::clock_counter_enabled() {
  return dma::is_buffer_timer_enabled(*driver_, dma_event_);
}

static void check_input_dims(const Index* program_in_dims,
                             const Shape& inputs_shape) {
  bool valid_dims = true;
  switch (inputs_shape.size()) {
    case 1:  // fully connected, 1 dimension
      if (inputs_shape[0] !=
          program_in_dims[0] * program_in_dims[1] * program_in_dims[2]) {
        valid_dims = false;
      }
      break;
    case 3:  // other cases (check only that data size is compatible)
      if (inputs_shape[0] * inputs_shape[1] * inputs_shape[2] !=
          program_in_dims[0] * program_in_dims[1] * program_in_dims[2]) {
        valid_dims = false;
      }
      break;
    default:
      valid_dims = false;
      break;
  }
  if (!valid_dims) {
    panic("Invalid input dimensions for this program");
  }
}

// reset whole akida core, including DMAs
static void core_reset(HardwareDriver* driver) {
  const auto top_level_reg_offset = driver->top_level_reg();
  auto reg_gen_ctrl =
      driver->read32(top_level_reg_offset + REG_GENERAL_CONTROL);
  // Reset NP & CORE
  set_field(&reg_gen_ctrl, AK_CORE_RST, 1);
  set_field(&reg_gen_ctrl, SCC_CORE_RESET, 1);
  driver->write32(top_level_reg_offset + REG_GENERAL_CONTROL, reg_gen_ctrl);
  // 20 cycles should be waited. Waiting 1ms is more than enough.
  msleep(1);
  // Fields need to be reset to 0
  set_field(&reg_gen_ctrl, AK_CORE_RST, 0);
  set_field(&reg_gen_ctrl, SCC_CORE_RESET, 0);
  driver->write32(top_level_reg_offset + REG_GENERAL_CONTROL, reg_gen_ctrl);
  // 40 cycles should be waited. Waiting 1ms is more than enough.
  msleep(1);
}

void HardwareDeviceImpl::init() {
  // this core reset is only available on production chip
  core_reset(driver_);

  // reset dmas
  reset_dma_engines();

  // reset epg
  epg::epg_reset(driver_);

  // init mesh
  if (mesh_ == nullptr) {
    // we need to allocate descriptors for DMA config, because discover uses it
    // to gather NPs information
    // Config dma descriptors are processed one at a time, but 2 descriptors
    // will need to be reserved because dma field DMA_MAX_DESC_CONTS needs to be
    // set to at least 1.
    alloc_dma_descriptors(driver_, &dma_config_.engine, &mem_mgr_,
                          dma::kMinNbDescriptors);
    mesh_ = mesh::discover(this);
    free_dma_descriptors(&dma_config_.engine, &mem_mgr_);
  }

  // reset HW mesh
  reset_nps_logic_and_cfg(driver_);

  // Pipeline is on by default
  pipeline(true);
}

static inline const int32_t* get_label(const std::vector<int32_t>& labels,
                                       size_t index) {
  return labels.size() == 1 ? &labels[0] : &labels[index];
}

std::vector<TensorUniquePtr> HardwareDeviceImpl::forward_loop(
    const std::vector<TensorConstPtr>& inputs,
    const std::vector<int32_t>* labels) {
  std::vector<TensorUniquePtr> result;

  result.reserve(inputs.size());
  size_t nb_inputs_queued = 0;

  // used to detect eventual timeout
  auto last_output_read = time_ms();
  static constexpr int32_t timeout = 5000;  // 5s timeout

  // store converted inputs that need to be kept alive while they have not been
  // processed
  std::vector<TensorUniquePtr> converted_inputs;
  const Tensor* input_to_queue;

  // loop until all outputs have been read
  while (result.size() < inputs.size()) {
    // keep system alive
    kick_watchdog();
    // enqueue as many jobs as current pipeline allow us
    bool pipeline_ready = true;
    while (nb_inputs_queued < inputs.size() && pipeline_ready) {
      // get label that could be the same for all inputs
      const int32_t* label = nullptr;
      if (labels != nullptr && labels->size() > 0) {
        label = get_label(*labels, nb_inputs_queued);
      }
      const auto& current_input = *inputs[nb_inputs_queued];
      // convert input if needed
      if (program::input_is_dense(current_program_.first)) {
        // dense input
        input_to_queue = conversion::as_dense(current_input);
        if (input_to_queue == nullptr) {
          converted_inputs.push_back(
              conversion::to_dense(static_cast<const Sparse&>(current_input)));
          input_to_queue = converted_inputs.back().get();
        }
      } else {
        // sparse input
        input_to_queue = conversion::as_sparse(current_input);
        if (input_to_queue == nullptr) {
          converted_inputs.push_back(
              conversion::to_sparse(static_cast<const Dense&>(current_input),
                                    current_program_.first));
          input_to_queue = converted_inputs.back().get();
        }
      }
      // try to enqueue
      pipeline_ready = enqueue(*input_to_queue, label);
      // if input was inserted, increment counter
      if (pipeline_ready) {
        ++nb_inputs_queued;
      }
    }
    // then read outputs that are ready
    bool output_ready = true;
    while (output_ready) {
      auto output = fetch();
      output_ready = output != nullptr;
      // if an output was ready, increment counter
      if (output_ready) {
        result.push_back(std::move(output));
        last_output_read = time_ms();
      } else if (time_ms() - last_output_read > timeout) {
        panic("Fatal error: timed out while fetching output");
      }
    }
  }
  return result;
}

const np::Mesh& HardwareDeviceImpl::mesh() const { return *mesh_; }

static void toggle_multi_pass(HardwareDeviceImpl* device,
                              bool enable_multi_pass) {
  auto driver = device->driver();
  const auto top_level_reg_offset = driver->top_level_reg();
  auto reg_gen_ctrl =
      driver->read32(top_level_reg_offset + REG_GENERAL_CONTROL);
  // toggle partial reconfig bit at top level register
  set_field(&reg_gen_ctrl, PR_MESH_RST_END, enable_multi_pass ? 1 : 0);
  driver->write32(top_level_reg_offset + REG_GENERAL_CONTROL, reg_gen_ctrl);
}

void HardwareDeviceImpl::unprogram() {
  // Do nothing if device is not programmed
  if (current_program_.first == nullptr) {
    return;
  }

  // free input dma memory
  auto& input_dma =
      program::input_is_dense(current_program_.first) ? dma_hrc_ : dma_event_;
  free_dma_descriptors(&input_dma.engine, &mem_mgr_);
  // free config dma memory
  free_dma_descriptors(&dma_config_.engine, &mem_mgr_);
  // rewind the whole program
  program::rewind(this, current_program_.first);
  // disable partial reconfig and reset DMAs to go back to default
  if (program::is_multi_pass(current_program_.first)) {
    toggle_multi_pass(this, false);
    // free multi pass memory
    multi_pass_memory_.free_memory(&mem_mgr_);
    // Core reset is necessary to avoid certains timeouts observed when
    // switching to single pass. These are probably due to an internal sync
    // issue between DMAs, but the core reset seems to be enough to fix the
    // problem.
    core_reset(driver_);
  }

  bool cc_enabled = clock_counter_enabled();
  // Reset the hardware device Mesh
  reset_nps_logic_and_cfg(driver_);
  // Reset dmas. It is required because instabilities have been observed when
  // switching descriptors base address without a reset beforehand, leading to
  // dma not taking account of the new descriptor base address
  reset_dma_engines();
  // If clock counter was enabled, re enable it (it was reset & turned off by
  // DMA reset)
  if (cc_enabled) {
    toggle_clock_counter(true);
  }

  current_program_ = {nullptr, 0};
  current_program_learn_en_ = false;

  // reset external memory in case of leftovers due to previous exception
  // it must be reset before MemoryManager or its entries might be already
  // free'd
  external_mem_.reset();
  // reset memory in case of leftovers due to previous exception
  mem_mgr_.reset();
}

void HardwareDeviceImpl::program(const uint8_t* program, size_t size,
                                 bool learn_en) {
  if (!program) {
    panic("program should not be null");
  }
  bool reprogram = (current_program_.first != program);

  const auto can_learn = program::can_learn(program);
  if (learn_en && !can_learn) {
    panic("program cannot learn");
  }
  auto& input_dma = program::input_is_dense(program) ? dma_hrc_ : dma_event_;

  if (reprogram) {
    // verify program validity
    program::verify(*this, program, size);
    // Unprogram the previous mapping
    unprogram();

    // allocate config dma descriptors
    // Config dma descriptors are processed one at a time, but 2 descriptors
    // will need to be reserved because dma field DMA_MAX_DESC_CONTS needs to be
    // set to at least 1.
    alloc_dma_descriptors(driver_, &dma_config_.engine, &mem_mgr_,
                          dma::kMinNbDescriptors);
    // allocate input dma descriptors
    alloc_dma_descriptors(driver_, &input_dma.engine, &mem_mgr_,
                          dma::kMaxNbDescriptors);

    // Set multi pass mode
    bool multi_pass_en = program::is_multi_pass(program);
    toggle_multi_pass(this, multi_pass_en);
    if (multi_pass_en) {
      // alloc required multi pass memory
      multi_pass_memory_.alloc_memory(&mem_mgr_, program);
      // configure config DMA for multipass
      program::play_multi_pass(this, program, &multi_pass_memory_);
      // configure inputs DMA for multipass
      dma::prepare_engine_multi_pass(
          driver_, input_dma, multi_pass_memory_.hw_generated_descriptor_addr,
          multi_pass_memory_.hw_generated_descriptor_out_addr,
          program::num_passes(program));
    } else {
      program::play_single_pass(this, program);
    }

    if (version() != NSoC_v2) {
      // When using dense/sparse outputs, we need to enable/disable the output
      // buffer automatic clearing from the input dma
      uint32_t clear_size =
          program::output_is_dense(program)
              ? static_cast<uint32_t>(
                    output_memory_required(program) -
                    dma::kOutputHeaderByteSize)  // we need to substract header
                                                 // size
              : 0;
      set_output_buffer_clear(driver_, input_dma, clear_size);
    }

    // pipeline state must be reset with the corresponding DMA last job id
    // processed
    pipeline_state_.reset(dma::get_last_job_id_processed(driver_, input_dma));

    current_program_ = {program, size};
  }
  if (can_learn) {
    // Learning mode is set independently as it can be modified without
    // reprogramming
    if (program::is_multi_pass(program)) {
      program::configure_learning_mode_multi_pass(this, program,
                                                  multi_pass_memory_, learn_en);
    } else {
      program::configure_learning_mode_single_pass(this, program, learn_en);
    }
  }

  // Pipeline can only be enabled in single pass if learn is disabled
  this->pipeline(!program::is_multi_pass(program) && !learn_en);

  current_program_learn_en_ = learn_en;
}

std::vector<TensorUniquePtr> HardwareDeviceImpl::predict(
    const std::vector<TensorConstPtr>& inputs) {
  // Check the device had been programmed
  if (!current_program_.first) {
    panic("Cannot predict without a program");
  }
  if (program::activation(current_program_.first)) {
    panic("Evaluate requires activations to be disabled");
  }
  if (current_program_learn_en_) {
    panic("Learn must be disabled to call the predict method.");
  }

  // first process all outputs
  auto outputs = forward_loop(inputs, nullptr);

  // Prepare results vector
  std::vector<TensorUniquePtr> result;
  result.reserve(outputs.size());
  for (Index i = 0; i < outputs.size(); i++) {
    // Outputs should be dense
    auto potentials = conversion::as_dense(*outputs[i]);
    assert(potentials);

    result.push_back(dequantize(*potentials));
  }

  return result;
}

bool HardwareDeviceImpl::enqueue(const Tensor& input, const int32_t* label) {
  if (!current_program_learn_en_ && label != nullptr) {
    panic("Learn must be enable to call enqueue with a label");
  }

  // in multi pass, we can only enqueue 1 descriptor at a time
  const auto is_multi_pass = program::is_multi_pass(current_program_.first);
  const auto pipeline_size = is_multi_pass ? 1 : dma::MAX_PIPELINE_SIZE;

  // check if there is space left in pipeline
  if (pipeline_state_.current_number_of_jobs() >= pipeline_size) {
    // pipeline is full, return false
    return false;
  }

  // check if input is in the correct format
  const auto input_is_dense = program::input_is_dense(current_program_.first);
  if (input_is_dense) {
    const auto* dense_input = conversion::as_dense(input);
    if (dense_input == nullptr) {
      panic("Input should be converted to Dense format before calling enqueue");
    }
  } else {
    const auto* sparse_input = conversion::as_sparse(input);
    if (sparse_input == nullptr) {
      panic(
          "Input should be converted to Sparse format before calling "
          "enqueue");
    }
  }

  // check if input dimensions are as expected
  const auto in_dims = program::input_dims(current_program_.first);
  check_input_dims(in_dims, input.dimensions());

  // reserve input address
  auto address_in =
      external_mem_.reserve(input.buffer()->data(), input.buffer()->size());
  // commit buffer
  external_mem_.commit(input.buffer()->data(), input.buffer()->size());
  // allocate output buffer in scratch buffer (must be 4 bytes aligned)
  const auto out_dims = program::output_dims(current_program_.first);
  const auto out_buffer_size = output_memory_required(current_program_.first);
  const auto address_out = mem_mgr_.alloc(out_buffer_size);

  // determine which dma controller should be used for inputs
  const auto& dma_inputs = select_dma_engine(input_is_dense);

  // Job id is the next one that should be processed.
  uint16_t job_id = pipeline_state_.new_job_id();

  // learn class is label + 1, or 0 if no label
  uint32_t learn_class = label != nullptr ? *label + 1 : 0;

  // generate descriptor
  const auto descriptor =
      input_is_dense
          ? dma_dense_descriptor(
                address_in, address_out, job_id, learn_class, in_dims,
                program::dense_window_w(current_program_.first),
                program::dense_window_h(current_program_.first))
          : dma::format_event_desc(
                job_id, address_in, address_out,
                static_cast<uint32_t>(input.buffer()->size() /
                                      sizeof(dma::w32)),
                learn_class);

  // in multi pass, we have to set output address in the input DMA since we're
  // using HW generated address
  if (is_multi_pass) {
    driver_->write32(
        dma_inputs.engine.reg_base_addr + DMA_REPLAY_OB_EVENT_BUF_ADDR_REG,
        address_out);
  }

  // store job information.
  pipeline_state_.enqueue_job(job_id, address_out, input.buffer()->data());

  // send descriptor to dma
  dma::enqueue_descriptor(driver_, dma_inputs.engine, descriptor);

  return true;
}

TensorUniquePtr HardwareDeviceImpl::fetch() {
  // if queue is empty, return null
  if (pipeline_state_.current_number_of_jobs() == 0) {
    return nullptr;
  }

  // select input dma
  const auto& input_dma =
      program::input_is_dense(current_program_.first) ? dma_hrc_ : dma_event_;

  if (program::is_multi_pass(current_program_.first)) {
    // in multi pass, there is only 1 job at a time so we just check for an
    // interrupt
    if (!dma::check_for_interrupt(driver_, input_dma.engine,
                                  DMA_BUFFER_END_STATUS_DESC_BURST_DONE)) {
      // no interrupt, output is not ready yet
      return nullptr;
    }
    // clear interrupts
    dma::clear_interrupts(driver_, input_dma.engine);
  } else {
    // in single pass, we need to check that last processed job id changed
    if (pipeline_state_.last_job_fetched() ==
        dma::get_last_job_id_processed(driver_, input_dma)) {
      return nullptr;
    }
  }

  // pop job from the queue
  auto job = pipeline_state_.pop_job();

  // free input
  external_mem_.release(job.input);

  // read output
  auto result = dma_events_read_outputs(
      driver_, job.output_address, program::output_dims(current_program_.first),
      program::output_format(current_program_.first));

  // free output
  mem_mgr_.free(job.output_address);

  return result;
}

DenseUniquePtr HardwareDeviceImpl::dequantize(const Dense& potentials) {
  // Get potentials strides and data from program
  auto shifts = program::shifts(current_program_.first);
  auto scales = program::scales(current_program_.first);
  assert(shifts.second == scales.second);
  const auto& shift = shifts.first;
  const auto& scale = scales.first;

  // perform sanity checks
  const auto coords = potentials.dimensions();
  if (coords.size() != 3) {
    panic("dequantize expects a 3D Dense");
  }
  if (potentials.layout() != Dense::Layout::RowMajor) {
    panic("dequantize expects a RowMajor Dense");
  }
  if (potentials.type() != TensorType::int32) {
    panic("dequantize expects an int32 Dense");
  }

  // Get potentials strides and data to access them via linear index
  const auto pot_strides = potentials.strides();
  const auto pot_data = potentials.data<int32_t>();
  // Allocate a dense output in the form of a RowMajor Tensor
  auto rescaled_outputs =
      Dense::create(TensorType::float32, coords, Dense::Layout::RowMajor);
  // Get rescaled outputs data
  const auto resc_data = rescaled_outputs->data<float>();
  for (Index x = 0; x < coords[0]; x++) {
    for (Index y = 0; y < coords[1]; y++) {
      // move pointer at the beginning of the neuron
      Index coord_n0[] = {x, y, 0};
      auto coord_lin_index_n0 = linear_index(coord_n0, pot_strides);
      auto poti = &pot_data[coord_lin_index_n0];
      auto resci = &resc_data[coord_lin_index_n0];
      for (Index n = 0; n < coords[2]; n++) {
        // Evaluate rescaled output
        auto value = static_cast<float>(poti[n] - shift[n]) / scale[n];
        // Set rescaled value at the same index than output
        resci[n] = value;
      }
    }
  }

  return rescaled_outputs;
}

size_t HardwareDeviceImpl::learn_mem_size() const {
  return program::learn_mem_size(current_program_.first);
}

void HardwareDeviceImpl::learn_mem(uint32_t* output_buffer) {
  if (!current_program_learn_en_) {
    panic("learn is not enabled");
  }
  program::learn_mem(this, current_program_.first, output_buffer);
}

void HardwareDeviceImpl::update_learn_mem(const uint32_t* input_buffer) {
  program::update_learn_mem(this, current_program_.first, input_buffer);
}

}  // namespace akida
