#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ipminify import IPv4

import unittest


class IPv4TestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(IPv4TestCase, self).__init__(*args, **kwargs)

        self.default_alphabet = IPv4.MINIFIER_ALPHABET

    def setUp(self):
        try:
            IPv4.set_default_alphabet(self.default_alphabet)
        except:
            self.fail("Unable to reset default alphabet.")

    def tearDown(self):
        try:
            IPv4.set_default_alphabet(self.default_alphabet)
        except:
            self.fail("Unable to reset default alphabet.")

    def test_class_vars(self):
        """Test that class vars are consistent and as expected."""
        self.assertEqual('abcdefghjkmnpqrstuvwxyz23456789', IPv4.MINIFIER_ALPHABET)
        self.assertEqual(len('abcdefghjkmnpqrstuvwxyz23456789'), IPv4.MINIFIER_ALPHABET_LEN)
        self.assertEqual(4, IPv4.MINIFIER_ALPHABET_MAP.get('e', None))
        self.assertEqual(IPv4.MINIFIER_ALPHABET_LEN, len(IPv4.MINIFIER_ALPHABET_MAP))

        # prevent lookalike chars
        self.assertFalse('i' in IPv4.MINIFIER_ALPHABET_MAP)
        self.assertFalse('1' in IPv4.MINIFIER_ALPHABET_MAP)
        self.assertFalse('l' in IPv4.MINIFIER_ALPHABET_MAP)
        self.assertFalse('I' in IPv4.MINIFIER_ALPHABET_MAP)
        self.assertFalse('o' in IPv4.MINIFIER_ALPHABET_MAP)
        self.assertFalse('O' in IPv4.MINIFIER_ALPHABET_MAP)
        self.assertFalse('0' in IPv4.MINIFIER_ALPHABET_MAP)

    def test_from_minified(self):
        """Tests that hydrating minified values works as expected."""
        self.assertEqual(IPv4(0x00000000), IPv4.from_minified('a'))
        self.assertEqual(IPv4(0x01020304), IPv4.from_minified('vkvju'))
        self.assertEqual(IPv4(0x7f000001), IPv4.from_minified('cpqe4kv'))
        self.assertEqual(IPv4(0xFFFFFFFF), IPv4.from_minified('e5aw83d'))

    def test_from_minified_with_alphabet(self):
        """Tests that hydrating minified values with a user-supplied alphabet works as expected."""
        ALPHA = '01'
        self.assertEqual(IPv4(0x00000000), IPv4.from_minified('0', ALPHA))
        self.assertEqual(IPv4(0x00000001), IPv4.from_minified('1', ALPHA))
        self.assertEqual(IPv4(0x00000002), IPv4.from_minified('10', ALPHA))
        self.assertEqual(IPv4(0x00000003), IPv4.from_minified('11', ALPHA))
        self.assertEqual(IPv4(0x00000004), IPv4.from_minified('100', ALPHA))
        self.assertEqual(IPv4(0x00000005), IPv4.from_minified('101', ALPHA))
        self.assertEqual(IPv4(0x00000006), IPv4.from_minified('110', ALPHA))
        self.assertEqual(IPv4(0x00000007), IPv4.from_minified('111', ALPHA))
        self.assertEqual(IPv4(0x00000008), IPv4.from_minified('1000', ALPHA))

    def test_from_minified_errors(self):
        """Tests that hydration throws appropriate errors."""
        try:
            IPv4.from_minified(None)
            self.fail("Failed to raise an exception on None value.")
        except ValueError:
            pass

        try:
            IPv4.from_minified({})
            self.fail("Failed to raise an exception on a non-string type.")
        except TypeError:
            pass

        try:
            IPv4.from_minified('')
            self.fail("Failed to raise an exception on an empty string.")
        except ValueError:
            pass

        # test alphabet edge cases
        try:
            IPv4.from_minified('a', {})
            self.fail("Failed to raise an exception on a non-string alphabet.")
        except TypeError:
            pass

        try:
            IPv4.from_minified('a', '')
            self.fail("Failed to raise an exception on an empty alphabet.")
        except ValueError:
            pass

        try:
            IPv4.from_minified('a', 'a')
            self.fail("Failed to raise an exception on a single-character alphabet.")
        except ValueError:
            pass

        # test value character not in alphabet
        try:
            IPv4.from_minified('z', 'abc')
            self.fail("Failed to raise an exception on a character not in alphabet.")
        except ValueError:
            pass

        # test decoding a value larger than a u32
        addr = IPv4(0xFFFFFFFF)
        addr._value += 1 # cause an overflow
        expanded = addr.minify()

        try:
            IPv4.from_minified(expanded)
            self.fail("Failed to raise exception on an integer out of u32 bounds.")
        except ValueError:
            pass

    def test_from_octets(self):
        """Tests that IPv4 address creation from octets works as expected."""
        self.assertEqual(0x00000000, IPv4.from_octets(0, 0, 0, 0).to_int())
        self.assertEqual(0x01020304, IPv4.from_octets(1, 2, 3, 4).to_int())
        self.assertEqual(0x7f000001, IPv4.from_octets(127, 0, 0, 1).to_int())
        self.assertEqual(0xFFFFFFFF, IPv4.from_octets(255, 255, 255, 255).to_int())

    def test_from_octets_errors(self):
        """Tests that creation of addresses from octets throws approprate errors."""
        oob_msg = "Should have failed with an out-of-bounds."

        # out of upper bound
        try:
            IPv4.from_octets(256, 0, 0, 0)
            self.fail(oob_msg)
        except ValueError:
            pass

        # out of lower bound
        try:
            IPv4.from_octets(0, 0, -1, 0)
            self.fail(oob_msg)
        except ValueError:
            pass

        # type
        try:
            IPv4.from_octets("BANANA", 0, 0, 0)
            self.fail("Should have failed with wrong type.")
        except TypeError:
            pass

    def test_from_str(self):
        """Tests that conversion from string values works as expected."""
        self.assertEqual(0x00000000, IPv4.from_str('0.0.0.0').to_int())
        self.assertEqual(0x01020304, IPv4.from_str('1.2.3.4').to_int())
        self.assertEqual(0xa0a0a0a, IPv4.from_str('10.10.10.10').to_int())
        self.assertEqual(0x7f000001, IPv4.from_str('127.0.0.1').to_int())
        self.assertEqual(0xFFFFFFFF, IPv4.from_str('255.255.255.255').to_int())

    def test_from_str_errors(self):
        """Tests that string conversion throws appropriate errors."""
        # incorrect type
        try:
            IPv4.from_str({})
            self.fail("Failed to raise a TypeError for a non-string value.")
        except TypeError:
            pass

        # incorrect string
        try:
            IPv4.from_str("NOPE")
            self.fail("Failed to raise a ValueError for an incorrect string.")
        except ValueError:
            pass

        # right format, not integers
        try:
            IPv4.from_str("A.B.C.D")
            self.fail("Failed to raise a ValueError for an incorrect period-delimited string.")
        except ValueError:
            pass

        # right format, integers out of bounds
        try:
            IPv4.from_str("1000.1.2.3")
            self.fail("Failed to raise a ValueError for an integer octet out of range.")
        except ValueError:
            pass

    def test_set_default_alphabet(self):
        """Tests that setting the default alphabet correctly sets class variables."""
        IPv4.set_default_alphabet('01')

        self.assertEqual('01', IPv4.MINIFIER_ALPHABET)
        self.assertEqual(2, IPv4.MINIFIER_ALPHABET_LEN)
        self.assertEqual({ '0': 0, '1': 1 }, IPv4.MINIFIER_ALPHABET_MAP)

    def test_set_default_alphabet_errors(self):
        """Tests that setting the default alphabet throws appropriate errors."""
        try:
            IPv4.set_default_alphabet(None)
            self.fail("Failed to raise a TypeError when passed a non-string type.")
        except TypeError:
            pass

        try:
            IPv4.set_default_alphabet('')
            self.fail("Failed to raise a ValueError when passed an empty string.")
        except ValueError:
            pass

        try:
            IPv4.set_default_alphabet('a')
            self.fail("Failed to raise a ValueError when passed a single-character alphabet.")
        except ValueError:
            pass

    def test_constructor(self):
        """Tests that constructor behaves as expected."""
        self.assertEqual(0xa0000001, IPv4(0xa0000001).to_int())

    def test_constructor_errors(self):
        """Tests that the constructor throws appropriate errors."""
        oob_msg = "Constructor should have failed with an out-of-bounds."

        # out of upper bound
        try:
            IPv4(0xFFFFFFFF + 1)
            self.fail(oob_msg)
        except ValueError:
            pass

        # out of lower bound
        try:
            IPv4(-1)
            self.fail(oob_msg)
        except ValueError:
            pass

        # wrong type
        try:
            IPv4({})
            self.fail("Constructor should have failed with wrong type.")
        except TypeError:
            pass

    def test___eq__(self):
        """Test equality operator."""
        # same type comparison
        self.assertEqual(IPv4(0x01020304), IPv4(0x01020304))
        self.assertNotEqual(IPv4(0x01020304), IPv4(0x02030405))
        # integer comparison
        self.assertEqual(0x01020304, IPv4(0x01020304))
        self.assertNotEqual(0x01020304, IPv4(0x02030405))
        # string comparison
        self.assertEqual('1.2.3.4', IPv4(0x01020304))
        self.assertNotEqual('1.2.3.4', IPv4(0x02030405))
        self.assertNotEqual('1000.1.-1.2', IPv4(0x00000000))

    def test___repr__(self):
        """Tests that the unambiguous string representation of the type is as expected."""
        self.assertEqual("IPv4(10.10.10.10)", repr(IPv4(0xa0a0a0a)))

    def test___str__(self):
        """Tests that the string representation of the type is as expected."""
        self.assertEqual("10.10.10.10", str(IPv4(0xa0a0a0a)))

    def test_minify(self):
        """Tests minification with the default alphabet."""
        self.assertEqual('a', IPv4(0x00000000).minify())
        self.assertEqual('vkvju', IPv4(0x01020304).minify())
        self.assertEqual('cpqe4kv', IPv4(0x7f000001).minify())
        self.assertEqual('e5aw83d', IPv4(0xFFFFFFFF).minify())

    def test_minify_with_alphabet(self):
        """Tests minification with a user-supplied alphabet."""
        ALPHA = '01'
        self.assertEqual('0', IPv4(0x00000000).minify(ALPHA))
        self.assertEqual('1', IPv4(0x00000001).minify(ALPHA))
        self.assertEqual('10', IPv4(0x00000002).minify(ALPHA))
        self.assertEqual('11', IPv4(0x00000003).minify(ALPHA))
        self.assertEqual('100', IPv4(0x00000004).minify(ALPHA))
        self.assertEqual('101', IPv4(0x00000005).minify(ALPHA))
        self.assertEqual('110', IPv4(0x00000006).minify(ALPHA))
        self.assertEqual('111', IPv4(0x00000007).minify(ALPHA))
        self.assertEqual('1000', IPv4(0x00000008).minify(ALPHA))

    def test_minify_errors(self):
        """Tests error cases of minification."""
        try:
            IPv4(0).minify({})
            self.fail("Failed to raise a TypeError on wrong alphabet type.")
        except TypeError:
            pass

        try:
            IPv4(0).minify('')
            self.fail("Failed to raise a ValueError for an empty alphabet.")
        except ValueError:
            pass

        try:
            IPv4(0).minify('a')
            self.fail("Failed to raise a ValueError for a single-character alphabet.")
        except ValueError:
            pass

    def test_to_int(self):
        """Tests that to_int returns the integer representation of the IP address."""
        self.assertEqual(0xFF0102FE, IPv4(0xFF0102FE).to_int())

    def test_to_octets(self):
        """Tests that conversion to octets behaves as expected."""
        self.assertEqual((0, 0, 0, 0), IPv4(0x00000000).to_octets())
        self.assertEqual((1, 2, 3, 4), IPv4(0x01020304).to_octets())
        self.assertEqual((10, 10, 10, 10), IPv4(0xa0a0a0a).to_octets())
        self.assertEqual((127, 0, 0, 1), IPv4(0x7f000001).to_octets())
        self.assertEqual((255, 255, 255, 255), IPv4(0xFFFFFFFF).to_octets())

    def test_to_str(self):
        """Tests that conversion to string works as expected."""
        self.assertEqual("0.0.0.0", IPv4(0).to_str())
        self.assertEqual("1.2.3.4", IPv4(0x01020304).to_str())
        self.assertEqual("10.10.10.10", IPv4(0xa0a0a0a).to_str())
        self.assertEqual("127.0.0.1", IPv4(0x7f000001).to_str())
        self.assertEqual("255.255.255.255", IPv4(0xFFFFFFFF).to_str())

    def test_conversion_lifecycle(self):
        """Tests that conversion between types works as expected."""
        # IPv4 -> octets -> IPv4
        self.assertEqual(IPv4(0x01020304), IPv4.from_octets(*IPv4(0x01020304).to_octets()))
        # IPv4 -> str -> IPv4
        self.assertEqual(IPv4(0x01020304), IPv4.from_str(IPv4(0x01020304).to_str()))

    def test_minifier_lifecycle(self):
        """Tests that minification is a consistent operation."""
        self.assertEqual(IPv4(0x00000000), IPv4.from_minified(IPv4(0x00000000).minify()))
        self.assertEqual(IPv4(0xFFFFFFFF), IPv4.from_minified(IPv4(0xFFFFFFFF).minify()))
