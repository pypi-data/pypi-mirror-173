#pragma once

#include <cstddef>
#include <cstdint>
#include <queue>

namespace akida {

class PipelineState {
 public:
  // utility struct to store infos about dma jobs
  struct dma_job {
    uint32_t output_address;
    const void* input;
    uint16_t id;
  };

  PipelineState() : job_id_generated_(0), last_job_id_fetched_(0) {}
  size_t current_number_of_jobs() const { return current_jobs_.size(); }
  void enqueue_job(uint16_t id, uint32_t output_address,
                   const void* input_address) {
    current_jobs_.push(dma_job{output_address, input_address, id});
  }
  dma_job pop_job() {
    auto job = current_jobs_.front();
    current_jobs_.pop();
    // update last_job_id_fetched
    last_job_id_fetched_ = job.id;
    return job;
  }
  uint16_t new_job_id() {
    // increment job id first because it must start at 1 after reset to
    // differenciate it from last_job_id_fetched which start at 0
    ++job_id_generated_;
    return job_id_generated_;
  }
  uint16_t last_job_fetched() const { return last_job_id_fetched_; }
  // reset should be called when dma is reset, because last_job_id_fetched may
  // not correspond to dma last job id processed
  void reset(uint16_t last_job_id) {
    last_job_id_fetched_ = last_job_id;
    job_id_generated_ = last_job_id;
    // clear the queue
    current_jobs_ = std::queue<dma_job>();
  }

 protected:
  std::queue<dma_job> current_jobs_;

  uint16_t job_id_generated_;
  uint16_t last_job_id_fetched_;
};

}  // namespace akida
