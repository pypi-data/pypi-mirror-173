"""
Cython Compiled utilities to get substrings of characters in larger strings,
similar to Linux/UNIX/*NIX strings command.

For the moment the function provided works over str data types to avoid
having to implement a Unicode encodings parser (UTF-8/16/32), so decoding
should be done before calling it. That is usually done best with 
bytes.decode(encoding, errors='ignore') or passing the corresponding
argument to open() if reading directly from a file.
"""

__version__ = "0.3.0"

cpdef list ascii_str(str data, int matchlen=4):
    """
    Iterates of all Py_UCS4 values in the `data` str and matches them
    against the ranges [0x09-0x0d] and [0x20-0x7e] (all ASCII printable
    characters).
    Returns a list of str's with all all the sequences of `matchlen` or more
    in a row it finds.

    :param data: str to search over
    :param matchlen: int, how many characters in sequence must be printables
        for a match to be added to the result list
    :return: list[str] of results
    """
    cdef size_t count = 0
    cdef int p = -1
    cdef size_t i = 0
    cdef Py_UCS4 c
    cdef list results = []

    for i, c in enumerate(data):
        if (c >= ' ' and c <= '~') or (c >= '\x09' and c <= '\x0d'):
            if p == -1:
                p = i
            count += 1
        elif p != -1:
            if count >= matchlen:
                results.append(data[p:i])
            p = -1
            count = 0
    if count >= matchlen:
        results.append(data[p:])
    return results