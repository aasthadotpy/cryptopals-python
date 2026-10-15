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

- `fixed_xor(left: str, right: str) -> str`: the current solution accepts hex
  strings and returns the XOR result as hex text.
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
5. **Collect the XOR values with `bytes(...)`.** This preserves each byte,
   including leading zero bytes.
6. **Return `result.hex()` and print it directly.** The function now returns
   readable hex text, matching its `-> str` annotation.

The current solution constructs XOR bytes and returns their hex representation. This
recommended version also moves the length check after decoding:

```python
left_bytes = bytes.fromhex(left)
right_bytes = bytes.fromhex(right)
if len(left_bytes) != len(right_bytes):
    raise ValueError("Input buffers should be of equal length")
return bytes(a ^ b for a, b in zip(left_bytes, right_bytes)).hex()
```

The expression inside `bytes(...)` generates one XOR result for each byte pair.

### Trying and checking an input

Run `python3 cryptopals/set01/challenge02.py` from the repository root. Inputs
`0f00` and `f00f` should display
`XOR result:  ff0f`.

For the hex-string interface, an automatic check is:

```python
assert fixed_xor("0f00", "f00f") == "ff0f"
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
  It does not accept a byte buffer. Use the buffer's `.hex()` method instead.
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
buffer as hex. The current `fixed_xor()` returns `result.hex()`, is annotated
with `-> str`, and the console prints the returned string directly. Returning
raw bytes is an alternative design, with `.hex()` then applied by the caller.

## Challenge 3

### Goal and approach

Find the single byte used to XOR every byte of the ciphertext, and recover the
message. The [challenge](https://cryptopals.com/sets/1/challenges/3) suggests
scoring candidate messages by how much they resemble English.

XOR reverses itself: `(original_byte ^ key) ^ key == original_byte`. There are
only 256 possible byte values, so try every key, decrypt with it, and keep the
candidate with the highest English score.

### Libraries and functions

No imported library is needed for this initial approach.

- `bytes.fromhex(ciphertext)`: decodes the provided hex text into ciphertext
  bytes. This step alone does not decrypt the message.
- `range(256)`: generates all possible keys, from 0 through 255.
- `bytes(b ^ key for b in ciphertext_bytes)`: XORs each integer byte value with
  the same candidate key and constructs a new candidate message buffer.
- `english_score(candidate)`: a proposed helper that rewards English-looking
  bytes and penalizes unlikely ones.
- `candidate.lower()`: normalizes ASCII letter case for scoring; leaves the
  original candidate available for displaying with its original capitalization.
- `float("-inf")`: an initial best score below any finite candidate score.
- `.decode("ascii")`: displays the winning message as text if it is ASCII.
- `chr(best_key)`: shows the key as a character; the numeric key is what XOR uses.

### Steps and reasons

1. **Decode hex once.** The key acts on the underlying data, not the hex digits.
2. **Try each of the 256 keys.** A single-byte key has a small enough search
   space to examine completely.
3. **XOR every ciphertext byte with the candidate key.** The original encryption
   used that same key at every position; repeating XOR reverses it.
4. **Score each candidate as English.** Generating candidates alone cannot tell
   us which one is the intended message. Reward spaces and common letters and
   penalize nonprintable or non-ASCII bytes.
5. **Remember the highest score, key, and candidate.** These identify the best
   guess and its recovered message.
6. **Print the winning message and return the key.** The function currently
   prints the message as a bytes representation and returns an integer key,
   which the console then prints.

The current `english_score()` uses these weights:

- Space: +3.
- Common letters in `aeioutrshdln`: +2, after lowercasing.
- Other ASCII letters: +1.
- Everything else, including punctuation and digits: -5.

These rules are alternatives per byte, not cumulative rewards. This simple
heuristic selects the expected key for the supplied challenge input, but is not
a guarantee for arbitrary ciphertexts. More detailed letter-frequency scores
can improve it later.

### Checking the approach

- Verify the XOR reversal with `(65 ^ 42) ^ 42 == 65`.
- Check that `english_score(b"hello world")` exceeds the score of
  `bytes([0, 255, 1])`.
- Run the supplied ciphertext through all keys and inspect the top candidates.
  The best one should read as an English sentence.

### Mistakes / surprises and lessons

- A representation such as `b'\x1b773...'` is still encrypted data. Printable
  characters appear because Python uses readable ASCII characters when showing
  byte values; this does not mean the message has been decrypted.
- The current `find_single_byte_xor_key()` now searches all keys, prints the
  winning message bytes, and returns the integer key as annotated.
- Do not discard candidates simply because they are valid ASCII, or accept the
  first readable candidate. Score all keys and compare the results.
- Decode to text for display after evaluating the raw byte candidates. Some
  wrong keys produce bytes that cannot be decoded as ASCII.
- `message.lower()` converts uppercase ASCII letters to lowercase so they get
  the same score. Bytes are not inherently lowercase: they hold values 0–255.
- Iterating over `message` produces integers, so compare a space with
  `byte == ord(" ")` (or `byte == 32`), rather than `byte == " "`.
- The current scoring penalizes valid English punctuation and digits too.
  Giving these printable characters a neutral score is a possible refinement.

Add an entry for each challenge as you work through the set, covering the goal,
approach, libraries and functions, steps and reasons, example checks, mistakes,
and lessons learned.
