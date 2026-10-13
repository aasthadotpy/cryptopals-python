# Set 1 notes

## Challenge 1

### Goal and approach

Convert a hexadecimal string to a Base64 string. Both formats represent the
same underlying data, so the approach is: **hex text → raw bytes → Base64 text**.

For example, `"4869"` represents the bytes `b"Hi"`, which become `"SGk="` in
Base64. Encoding the characters `"4869"` directly would encode different data
and produce `"NDg2OQ=="`.

### Libraries and functions used

- `base64`: Python's standard-library module for Base64 encoding; no installation
  is needed.
- `hex_to_base64(hex_string: str) -> str`: our function that accepts hex text and
  returns Base64 text. The type hints describe the expected input and output;
  they do not enforce or validate the types at runtime.
- `bytes.fromhex(hex_string)`: a built-in method that interprets each pair of
  hexadecimal digits as one byte. For example, `48` becomes the byte for `H`.
- `base64.b64encode(byte_data)`: encodes the raw bytes as Base64 and returns bytes
  containing the encoded text.
- `.decode("ascii")`: converts those Base64 bytes to a Python string. ASCII is
  sufficient because all Base64 characters belong to the ASCII character set.
- `input(...)`: displays a prompt and returns the console input as a string.
- `print(...)`: displays the intermediate bytes and final result. The `f"..."`
  strings insert variable values into the displayed messages.

### Steps and why each is needed

1. **Import `base64`.** This makes Python's Base64 encoder available.
2. **Read the hex string with `input()`.** This lets us try different inputs
   without editing the code each time.
3. **Call `hex_to_base64(hex_string)`.** Keeping the conversion in a function
   makes it reusable and easy to check with known inputs.
4. **Convert hex text to bytes using `bytes.fromhex()`.** The encoder needs the
   actual data represented by the hex digits, rather than the characters used
   to write those digits.
5. **Print `byte_data`.** This is a debugging aid that helps us see the decoded
   data; it is optional and does not affect the conversion.
6. **Encode the bytes using `base64.b64encode()`.** This represents the same data
   using Base64 characters.
7. **Decode the encoded bytes with `.decode("ascii")`.** The function promises
   to return a string, while `b64encode()` returns bytes.
8. **Return and print the result.** `return` passes the value back to the caller;
   the final `print()` shows it in the console.

The `if __name__ == "__main__":` guard runs the console prompts only when this
file is run directly. Importing the function from another module or a test does
not trigger the prompts.

### Trying and checking an input

From the repository root, run:

```bash
python3 cryptopals/set01/challenge01.py
```

Example console session:

```text
Enter a hexadecimal string: 4869
Byte data: b'Hi'
Base64 result: SGk=
```

To check the result automatically, use a known input and expected output:

```python
assert hex_to_base64("4869") == "SGk="
```

An assertion raises `AssertionError` if the result differs from the expected
value. Invalid hex characters or an incomplete hex pair cause
`bytes.fromhex()` to raise `ValueError`; the current script does not catch it.

### Mistakes / surprises

- `byte_data.encode("base64")` does not work in Python 3. Use
  `base64.b64encode(byte_data)` instead.
- `b64encode()` does not append a newline, so `.rstrip("\n")` is unnecessary.
- The first conversion interprets hex text as data; the final `.decode()` turns
  the already encoded Base64 bytes into text. They serve different purposes.

### What I learned

Hex and Base64 are encodings, not encryption. Converting between them changes
how data is represented while preserving the underlying bytes. Python
distinguishes text (`str`) from binary data (`bytes`), so each conversion should
be explicit.

## Challenge 2

### Goal and approach

Combine two equal-length buffers with XOR. XOR produces a `1` bit where the
input bits differ and a `0` bit where they match. Apply it to each corresponding
pair of bytes, then display the result as hex.

### Libraries and functions used

No imported library is needed for the conversion and XOR operation.

- `fixed_xor(left: str, right: str) -> bytes`: the current solution accepts hex
  strings and intends to return raw bytes.
- `bytes.fromhex(...)`: converts each input hex string to its underlying bytes.
- `len(...)`: currently checks the input text lengths. Checking decoded buffer
  lengths instead is the recommended improvement below.
- `ValueError`: signals that the input lengths are incompatible.
- `zip(left_bytes, right_bytes)`: pairs bytes at the same position. Iterating
  over a `bytes` object yields integer values from 0 to 255.
- `a ^ b`: performs bitwise XOR on those integer values.
- `bytes(...)`: collects the resulting integer values into a byte buffer.
- `.hex()`: converts the result buffer to a hexadecimal string for display.
- `input(...)` and `print(...)`: read console inputs and display the result.

### Steps and reasons for the proposed correction

1. **Read two hex strings.** Hex makes binary inputs easy to type and inspect.
2. **Decode both with `bytes.fromhex()`.** XOR should operate on the represented
   data, rather than the characters used to write the hex strings.
3. **Compare the decoded lengths.** The buffers must have equal byte counts.
   Checking text length can be misleading because `bytes.fromhex()` accepts
   whitespace. This check also prevents `zip()` from silently stopping at the
   end of the shorter buffer.
4. **Pair the bytes with `zip()` and XOR each pair.** Python supports `^` for
   integers, but not directly for whole `bytes` objects.
5. **Collect the XOR values with `bytes(...)` and return them.** This matches
   the function's `-> bytes` annotation and preserves each byte, including
   leading zero bytes.
6. **Call `.hex()` when printing.** Keep the result as raw bytes inside the
   function and convert it to readable hex at the console boundary.

The current solution now constructs and returns the XOR bytes correctly. This
recommended version also moves the length check after decoding:

```python
left_bytes = bytes.fromhex(left)
right_bytes = bytes.fromhex(right)
if len(left_bytes) != len(right_bytes):
    raise ValueError("Input buffers should be of equal length")
return bytes(a ^ b for a, b in zip(left_bytes, right_bytes))
```

The expression inside `bytes(...)` generates one XOR result for each byte pair.

### Trying and checking an input

Run `python3 cryptopals/set01/challenge02.py` from the repository root. Inputs
`0f00` and `f00f` should display
`XOR result:  ff0f`.

For the hex-string interface, an automatic check is:

```python
assert fixed_xor("0f00", "f00f").hex() == "ff0f"
```

The original implementation raised `TypeError` at
`left_bytes ^ right_bytes`; the current solution fixes this. The existing test in `tests/test_challenge02.py`
is skipped and passes raw bytes as inputs. It must be aligned with the chosen
interface before it can validate the solution: either use hex strings in that
test, or make the function accept bytes and decode console input before calling
it.

### Mistakes / surprises

- `left_bytes ^ right_bytes` fails because whole byte buffers do not support
  the `^` operator. XOR each pair of integer byte values instead.
- The built-in `hex()` accepts an integer and returns text with a `0x` prefix.
  It does not build a byte buffer. Wrapping the result in `hex()` conflicts
  with both the `-> bytes` annotation and the later `result.hex()` call.
- Validate buffer lengths after decoding, rather than comparing hex text
  lengths.
- The solution and test currently disagree about whether inputs are hex text
  or raw bytes.

### What I learned

A byte buffer is a sequence of integer byte values. Operations such as XOR can
be applied to those values individually, and `bytes(...)` assembles the results
back into a buffer. Input and output types must agree across the function,
console code, and tests.

### Clarifications: building bytes and displaying hex

Converting the inputs to bytes does not automatically make the XOR results a
byte buffer. Iterating over bytes yields integers, and XOR of two integers
produces another integer. For example:

```python
left_bytes = bytes.fromhex("0f00")   # integer values: 15, 0
right_bytes = bytes.fromhex("f00f")  # integer values: 240, 15
# XOR values: 15 ^ 240 = 255, and 0 ^ 15 = 15
result = bytes([255, 15])            # b'\xff\x0f'
assert result.hex() == "ff0f"
```

In `bytes(a ^ b for a, b in zip(left_bytes, right_bytes))`, the inner generator
yields these integer results, and the outer `bytes(...)` builds a new buffer
from them. It does not re-decode the input buffers.

In the [challenge wording](https://cryptopals.com/sets/1/challenges/2), “after
hex decoding” refers to decoding the input before XOR. The expected output is
shown in hex for readability. The full flow is:

```text
input hex text → bytes.fromhex() → input bytes → XOR → result bytes → .hex() → output hex text
```

`hex(255)` returns the string `"0xff"`, but `hex(result)` raises `TypeError`
because `result` is a byte buffer. Use `result.hex()` to represent a whole
buffer as hex. The console already does this, so returning raw bytes from
`fixed_xor()` is consistent. Returning `result.hex()` from the function is also
possible, but would require changing its return annotation to `str` and printing
that returned string directly.

Add an entry for each challenge as you work through the set, covering the goal,
approach, libraries and functions, steps and reasons, example checks, mistakes,
and lessons learned.
