'''
Set 1, challenge 1. Convert a hexadecimal string to a Base64 string.
'''

import base64


def hex_to_base64(hex_string: str) -> str:

    # Convert the hexadecimal string to bytes
    byte_data = bytes.fromhex(hex_string)
    print(f"Byte data: {byte_data}")
    
    # Encode the bytes to Base64
    base64_string = base64.b64encode(byte_data).decode("ascii")
    
    return base64_string

if __name__ == "__main__":
    hex_string = input("Enter a hexadecimal string: ")
    result = hex_to_base64(hex_string)
    print(f"Base64 result: {result}")