cpdef int fact(int x):
    cdef int res = 1
    cdef int i
    for i in range(1, x + 1):
        res += i
    return res