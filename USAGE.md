# Usage

Create an IPv4 address via a variety of different methods:

```python
>>> from ipminify import IPv4
>>> IPv4(0x7f000001) == IPv4.from_octets(127, 0, 0, 1) == IPv4.from_str('127.0.0.1')
True
```

Minify an IPv4 address using the default alphabet:

```python
>>> addr = IPv4.from_octets(127, 0, 0, 1)
>>> addr.minify()
'cpqe4kv'
```

Expand a minified address into an `IPv4` instance:

```python
>>> minified = IPv4.from_octets(127, 0, 0, 1).minify()
>>> IPv4.from_minified(minified)
IPv4(127.0.0.1)
```

And bring your own minifier alphabet if desired:

```python
>>> IPv4(127, 0, 0, 1).minify('abc')
'bcbbbbbbaccaaccacaac'
>>> IPv4.from_minified('bcbbbbbbaccaaccacaac', 'abc')
IPv4(127.0.0.1)
```

To globally set the default alphabet program-wide, execute the following during your program's initialization:

```python
from ipminify import IPv4

IPv4.set_default_alphabet('01') # binary
```

Additionally, as shown above, custom alphabets can be used whenever invoking a conversion function:

```python
>>> alphabet = '01'
>>> minified = IPv4.from_octets(127, 0, 0, 1).minify(alphabet)
>>> minified
'1111111000000000000000000000001'
>>> IPv4.from_minified(minified, alphabet)
IPv4(127.0.0.1)
```
