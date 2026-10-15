'''
Set 1, challenge 2:
Write a function that takes two equal-length buffers 
and produces their XOR combination
'''

def fixed_xor(left: str, right: str) -> str:

    if len(left) != len(right):
        raise ValueError("Input buffers should be of equal length")

    left_bytes = bytes.fromhex(left)
    right_bytes = bytes.fromhex(right)
    result = bytes(a ^ b for a,b in zip(left_bytes, right_bytes))

    return result.hex()

if __name__ == "__main__":
    left = input("Enter the first hex string: ")
    right = input("Enter the second hex string: ")
    result = fixed_xor(left, right)
    print("XOR result: ", result)
