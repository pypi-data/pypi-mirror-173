#pragma once
#include <cstddef>
#include <map>

#include "engine/dma.h"
#include "engine/memory_mgr.h"

#include "infra/hardware_driver.h"

namespace akida {

class ExternalMemoryMgr {
 public:
  explicit ExternalMemoryMgr(MemoryMgr* mgr, HardwareDriver* driver)
      : mem_mgr_(mgr), driver_(driver) {}

  // Allocate and keep track in ledger. To be used by program
  using AllocId = const void*;
  uint32_t reserve(AllocId id, size_t byte_size);

  // Free memory allocated with alloc and track
  void release(AllocId id);

  // get previously allocated address by id
  uint32_t tracked(AllocId id) const;

  // commit the memory to the device
  void commit(AllocId id, size_t size);

  // Free all memory allocations, to restore initial state
  void reset();

 private:
  // return non 0 value if id is directly accessible by akida, 0 otherwise
  dma::addr access_from_akida(AllocId id);

  // memory manager
  MemoryMgr* mem_mgr_;
  // hardware driver
  HardwareDriver* driver_;
  // allocation ledger, a map of id:addresss
  std::map<AllocId, uint32_t> alloc_ledger_;
};

}  // namespace akida
