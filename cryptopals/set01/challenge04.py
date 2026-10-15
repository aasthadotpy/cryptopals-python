'''
Detect single-character XOR
One of the 60-character strings in the file "./challenge-data/4.txt" 
has been encrypted by single-character XOR.

Find it.
'''

def english_score(candidate: bytes) -> int:

    score = 0

    for byte in candidate.lower():

        if byte == ord(" "):
            score += 3

        elif byte in b"aeioushtdnlr":
            score += 2

        elif ord("a") <= byte <= ord("z"):
            score += 1

        else:
            score -= 5

    return score

with open("/Users/aasthasingh/Desktop/Projects/cryptopals-python/cryptopals/challenge-data/4.txt", "r", encoding = "utf-8") as file:

    best_score = float("-inf")
    best_key = None
    best_candidate = None

    for line in file:
        #strip() removes surrounding whitespace, including newline
        hex_string = line.strip()
        hex_string_bytes = bytes.fromhex(hex_string)

        for byte in range(256):
            candidate = bytes(a ^ byte for a in hex_string_bytes)
            current_score = english_score(candidate)

            if current_score > best_score:
                best_score = current_score
                best_key = byte
                best_candidate = candidate

    print(best_key)
    print(chr(best_key))
    print(best_candidate)