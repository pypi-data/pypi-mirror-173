
Cross-Platform Aligned Data Structures
======================================

This is a C++11 header-only library providing various utility functions
and containers of aligned POD types. From the lowest level to the highest
level of abstraction, we have:

include/cpads/memory.hpp
------------------------

This exposes the function `void* hh::zalloc(uint64_t nbytes)` which
zero-allocates a block of a given number of bytes, aligned so that the
pointer is a multiple of 128 bytes. Unlike `posix_memalign`, this is
cross-platform and is guaranteed to zero out the returned memory.

To deallocate a pointer allocated by `hh::zalloc`, we provide `hh::zfree`.

include/cpads/ivector.hpp
-------------------------

This exposes a class `hh::ivector<typename T, int B = 8>` which differs
from a `std::vector` in the following respects:

 - backed by multiple arrays (of length $`2^B`$) instead of a single array;
 - individual arrays are aligned to a multiple of 128 bytes;
 - existing elements are never moved, even when the ivector is resized;
 - the memory overhead from repeated appending is small;
 - the ivector as a whole cannot be moved/copied.

It is recommended for backing large data structures of POD types, especially
those which are expected to occupy a large fraction of total available memory.


