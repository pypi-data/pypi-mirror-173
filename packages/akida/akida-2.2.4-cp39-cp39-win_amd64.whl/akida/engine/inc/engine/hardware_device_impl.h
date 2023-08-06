#pragma once

#include <cstddef>
#include <cstdint>
#include <memory>
#include <queue>
#include <vector>

#include "akida/hardware_device.h"
#include "akida/hw_version.h"
#include "akida/np.h"
#include "akida/tensor.h"
#include "engine/dma.h"
#include "engine/dma_engine.h"
#include "engine/external_mem_mgr.h"
#include "engine/memory_mgr.h"
#include "engine/multipass_memory.h"
#include "engine/pipeline_state.h"
#include "infra/hardware_driver.h"

namespace akida {

namespace dma {
// forward declarations
enum class Target;
}  // namespace dma

class HardwareDeviceImpl final : public HardwareDevice {
 public:
  HardwareDeviceImpl(HardwareDriver* driver);

  ~HardwareDeviceImpl();

  // Device API
  HwVersion version() const override;

  const char* desc() const override { return driver_->desc(); }

  void pipeline(bool enable);

  void toggle_clock_counter(bool enable) override;

  uint32_t read_clock_counter() override;

  const np::Mesh& mesh() const override;

  void dma_config_write(const dma::w32* buffer, size_t buffer_size);

  void dma_config_read(dma::w32* buffer, const struct np::Ident& np,
                       dma::Target target, uint16_t addr_target_word,
                       uint32_t nb_words);

  void dma_start_config_multipass(dma::addr conf_base_address,
                                  uint32_t num_descs, uint32_t num_passes,
                                  uint32_t num_extra_descs);

  // Device fit
  std::vector<TensorUniquePtr> fit(
      const std::vector<TensorConstPtr>& inputs,
      const std::vector<int32_t>& input_labels) override;

  // Device forward
  std::vector<TensorUniquePtr> forward(
      const std::vector<TensorConstPtr>& inputs) override;

  // Device predict
  std::vector<TensorUniquePtr> predict(
      const std::vector<TensorConstPtr>& inputs) override;

  // Queue input
  bool enqueue(const Tensor& input, const int32_t* label = nullptr) override;

  // check for output
  TensorUniquePtr fetch() override;

  // apply rescale
  DenseUniquePtr dequantize(const Dense& potentials) override;

  // perform hardware device programming
  void program(const uint8_t* program, size_t size, bool learn_en) override;

  // unprogram current program
  void unprogram() override;

  // Return the memory used currently in the device
  MemoryInfo memory() const override { return mem_mgr_.report(); }

  void reset_top_memory() override { mem_mgr_.reset_top_usage(); }

  const BytesBuffer& program() const override { return current_program_; }

  bool learn_enabled() const override { return current_program_learn_en_; }

  size_t learn_mem_size() const override;

  void learn_mem(uint32_t* output_buffer) override;

  void update_learn_mem(const uint32_t* input_buffer) override;

  HardwareDriver* driver() const override { return driver_; }

  MemoryMgr* mem() { return &mem_mgr_; }

  ExternalMemoryMgr* external_mem() { return &external_mem_; }

 private:
  HardwareDriver* driver_;
  HwVersion version_;
  std::unique_ptr<np::Mesh> mesh_;
  dma::Config dma_config_;
  dma::Inputs dma_event_;
  dma::Inputs dma_hrc_;
  MemoryMgr mem_mgr_;
  BytesBuffer current_program_;
  bool current_program_learn_en_;
  ExternalMemoryMgr external_mem_;

  // infos on memory that need to be allocated for multi pass program
  MultiPassMemory multi_pass_memory_;

  PipelineState pipeline_state_;

  // Initialization helpers
  void reset_dma_engines();
  void init();

  // pipeline helper
  std::vector<TensorUniquePtr> forward_loop(
      const std::vector<TensorConstPtr>& inputs,
      const std::vector<int32_t>* labels);

  // DMA helpers
  const dma::Inputs& select_dma_engine(bool is_hrc);
  bool clock_counter_enabled();
};

}  // namespace akida
