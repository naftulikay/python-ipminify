#!/usr/bin/env python
# -*- coding: utf-8 -*-

import six


class IPv4(object):
    """An IPv4 address utility class."""

    MINIFIER_ALPHABET = 'abcdefghjkmnpqrstuvwxyz23456789'
    MINIFIER_ALPHABET_LEN = len(MINIFIER_ALPHABET)
    MINIFIER_ALPHABET_MAP = { letter: index for index, letter in enumerate(MINIFIER_ALPHABET) }

    @classmethod
    def from_minified(cls, value, alphabet=None):
        """Convert a minified string representation into an IPv4 address, optionally with a user-supplied alphabet."""
        if value is None:
            raise ValueError("Unable to unmarshal minified value: value is None.")

        if not isinstance(value, six.string_types):
            raise TypeError("Value must be a string.")

        if len(value) == 0:
            raise ValueError("Value must contain at least one character.")

        if alphabet is not None:
            if not isinstance(alphabet, six.string_types):
                raise TypeError("Custom alphabet must be a string type.")

            if len(alphabet) < 2:
                raise ValueError("Custom alphabet must include at least two characters.")

            alphabet_len, alphabet_map = len(alphabet), { letter: index for index, letter in enumerate(alphabet) }
        else:
            alphabet, alphabet_len, alphabet_map = IPv4.MINIFIER_ALPHABET, IPv4.MINIFIER_ALPHABET_LEN, IPv4.MINIFIER_ALPHABET_MAP

        # do work
        result = 0

        for index, letter in enumerate(value):
            if alphabet_map.get(letter, -1) < 0:
                raise ValueError("Value contains letter not present in minifier alphabet: {}".format(letter))

            result = (result * alphabet_len) + alphabet_map[letter]

        try:
            return IPv4(result)
        except ValueError as e:
            raise ValueError("Unable to expand minified value, value is out of u32 bounds: {}".format(e))

    @classmethod
    def from_octets(cls, octet0, octet1, octet2, octet3):
        """Construct an IPv4 address from four octet integers."""
        result = 0x00000000 & 0xFFFFFFFF

        for index, octet in enumerate([octet0, octet1, octet2, octet3]):
            if not isinstance(octet, int):
                raise TypeError("Octet {} is not an integer: {}".format(index, octet))

            if octet < 0 or octet > 255:
                raise ValueError("Octet {} is out of bounds: {}".format(index, octet))

            result ^= octet

            if index < 3:
                result <<= 8

        return IPv4(result)

    @classmethod
    def from_str(cls, value):
        """Construct an IPv4 address from a period-delimited string."""
        if not isinstance(value, six.string_types):
            raise TypeError("Value {} is not a string.".format(value))

        octets = value.split('.')

        if len(octets) != 4:
            raise ValueError("Invalid IPv4 address string: {}".format(value))

        for index, octet in enumerate(octets):
            try:
                octets[index] = int(octet)
            except ValueError as e:
                raise ValueError("Unable to convert octet {} to an integer: {} ({})".format(index, octet, e))

        return IPv4.from_octets(*octets)

    @classmethod
    def set_default_alphabet(cls, alphabet):
        """Set the default alphabet globally."""
        if not isinstance(alphabet, six.string_types):
            raise TypeError("Alphabet must be a string, received {}".format(type(alphabet)))

        if len(alphabet) < 2:
            raise ValueError("Alphabet must contain at least two characters.")

        cls.MINIFIER_ALPHABET = alphabet
        cls.MINIFIER_ALPHABET_LEN = len(alphabet)
        cls.MINIFIER_ALPHABET_MAP = { letter: index for index, letter in enumerate(alphabet) }

    def __init__(self, value):
        """Construct an IPv4 address from an unsigned, 32-bit integer."""
        if not isinstance(value, int):
            raise TypeError("Value must be an integer.")

        if value < 0 or value > 0xFFFFFFFF:
            raise ValueError("IPv4 address not in range (0x00000000-0xFFFFFFFF): {}".format(hex(value)))

        self._value = value

    def __eq__(self, other):
        """Test equality against another object."""
        if isinstance(other, IPv4):
            return self.to_int() == other.to_int()
        elif isinstance(other, int):
            return self.to_int() == other
        elif isinstance(other, six.string_types):
            try:
                return self.to_int() == IPv4.from_str(other).to_int()
            except:
                return False
        else:
            return False

    def __repr__(self):
        """Return an unambiguous string representation of this IPv4 address."""
        return "IPv4({})".format(self.to_str())

    def __str__(self):
        """Return a readable representation of this IPv4 address."""
        return self.to_str()

    def minify(self, alphabet=None):
        """Convert this IPv4 address into a minified string, optionally with a user-supplied alphabet."""
        if alphabet is not None:
            if not isinstance(alphabet, six.string_types):
                raise TypeError("Alphabet must be a string.")

            if len(alphabet) < 2:
                raise ValueError("Alphabet must contain at least two characters.")

            alphabet_len, alphabet_map = len(alphabet), { letter: index for index, letter in enumerate(alphabet) }
        else:
            alphabet, alphabet_len, alphabet_map = IPv4.MINIFIER_ALPHABET, IPv4.MINIFIER_ALPHABET_LEN, IPv4.MINIFIER_ALPHABET_MAP

        # okay let's get to work
        value = self._value

        if value == 0:
            # short-circuit
            return alphabet[0]

        result = []

        while value > 0:
            value, rem = int(value / alphabet_len), value % alphabet_len
            result.append(alphabet[rem])

        return ''.join(reversed(result))


    def to_int(self):
        """Return an integer representation of this IPv4 address."""
        return self._value

    def to_octets(self):
        """Convert to a tuple of four octets as integers."""
        return (self._value >> 24, (self._value >> 16) & 0xFF, (self._value >> 8) & 0xFF, self._value & 0xFF)

    def to_str(self):
        """Convert to a period-delimited string."""
        return '.'.join(map(lambda i: str(i), self.to_octets()))
