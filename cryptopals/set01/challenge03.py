'''
Set 1, challenge 3:
Single-byte XOR cipher. The hex encoded string:

1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736

has been XOR'd against a single character. Find the key, decrypt the message.
'''

def find_single_byte_xor_key(ciphertext: str) -> int:

    # Decode the hex representation into the actual encrypted bytes.
    ciphertext_bytes = bytes.fromhex(ciphertext)

    best_score = float("-inf")
    best_key = None
    best_message = None

    # A single-byte key can have any integer value from 0 through 255.
    for key in range(256):

        # Iterating over bytes gives integers. XOR each with the same key,
        # then collect the resulting integers into a new byte buffer.
        candidate = bytes(a ^ key for a in ciphertext_bytes)

        # Higher scores indicate a candidate that looks more like English.
        score = english_score(candidate)

        if score > best_score:
            best_score = score
            best_key = key
            best_message = candidate

    print(best_message)
    return best_key

def english_score(message: bytes) -> int:
    score = 0

    # Normalize uppercase ASCII letters so H and h receive the same score.
    # Each loop value is still an integer, even when the bytes display as text.
    for byte in message.lower():

        # ord(" ") is 32: compare the byte value with an integer, not a string.
        if byte == ord(" "):
            score += 3
        # Membership in a bytes object checks for an integer byte value.
        # byte is iterating over integers 97 (a), 101 (e), 105 (i), 111 (o), 117 (u)...
        elif byte in b"aeioutrshdln":
            score += 2
        # Give a smaller reward to the remaining lowercase ASCII letters.
        elif ord("a") <= byte <= ord("z"):
            score += 1
        else:
            # This rule also penalizes punctuation and digits, not just nonprintable bytes
            score -= 5

    return score
    
if __name__ == "__main__":
    ciphertext = input("Enter the hex encoded ciphertext: ")
    result = find_single_byte_xor_key(ciphertext)
    print(result)  # The integer key
    print(chr(result)) # the character with ASCII value of result
