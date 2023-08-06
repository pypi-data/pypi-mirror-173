# nixstrings
Linux/UNIX/*NIX strings command, in Cython

Over the years I've found many programs in digital forensics need this kind of
functionality, some do it by piping strings with a subprocess, others use
regexes, others implement a listcomp of their own.

Of those, usually the regex is the fastest, but it turns out you can actually go
a bit faster with the help of C(ython).

This module has specialized functions that compile the comparisson of characters
values to get the results as fast as possible. On synthethic benchmarks, the
`ascii_strings()` function is almost 5x faster than the equivalent regex (that 
would be`rx = re.compile(f'[{ascii_printables}]{{4,}}')` and then 
`rx.findall(data)`), but on real case scenarios it's usually just 2x faster 
before I/O becomes the main bottleneck.
