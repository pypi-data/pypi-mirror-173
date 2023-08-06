#include "engine/external_mem_mgr.h"

#include <cstdint>

#include "engine/memory_mgr.h"
#include "infra/system.h"

namespace akida {

uint32_t ExternalMemoryMgr::reserve(AllocId id, size_t byte_size) {
  // prevent allocating if ledger already contains an entry
  if (alloc_ledger_.find(id) != alloc_ledger_.end()) {
    panic("Tracked allocation ID %p already taken", id);
  }

  // get address
  dma::addr addr = access_from_akida(id);

  // alloc memory if we need to
  if (addr == 0) {
    addr = mem_mgr_->alloc(byte_size);
  }

  // record in ledger
  alloc_ledger_[id] = addr;
  return addr;
}

void ExternalMemoryMgr::release(AllocId id) {
  auto addr = tracked(id);
  if (!access_from_akida(id)) {
    mem_mgr_->free(addr);
  }
  alloc_ledger_.erase(id);
}

uint32_t ExternalMemoryMgr::tracked(AllocId id) const {
  auto entry = alloc_ledger_.find(id);
  // check if item is not in ledger
  if (entry == alloc_ledger_.end()) {
    panic("Tracked allocation ID %p not found", id);
  }
  auto& addr = entry->second;
  return addr;
}

void ExternalMemoryMgr::commit(AllocId id, size_t size) {
  auto addr = tracked(id);
  if (!access_from_akida(id)) {
    driver_->write(addr, id, size);
  }
}

void ExternalMemoryMgr::reset() {
  // free all elements, in reverse order
  for (auto iter = alloc_ledger_.rbegin(); iter != alloc_ledger_.rend();
       ++iter) {
    // free only memory that has been allocated by us
    if (!access_from_akida(iter->first)) {
      mem_mgr_->free(iter->second);
    }
  }
  // clear up map
  alloc_ledger_.clear();
}

dma::addr ExternalMemoryMgr::access_from_akida(AllocId id) {
  if ((sizeof(AllocId) == sizeof(dma::addr)) &&
      (driver_->akida_visible_memory() != 0)) {
    // we can safely cast because dma::addr and AllocId types have the same size
    auto addr32 = static_cast<dma::addr>(reinterpret_cast<size_t>((id)));
    // if the address is in embedded data range we can use it directly
    if (addr32 >= driver_->akida_visible_memory() &&
        addr32 <= (driver_->akida_visible_memory() +
                   driver_->akida_visible_memory_size())) {
      return addr32;
    }
  }
  // cannot access from akida
  return 0;
}

}  // namespace akida
