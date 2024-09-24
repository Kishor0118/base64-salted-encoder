import base64

def encode_with_salt(payload: str, salt_key: str, salt_index: int) -> str:
    # Convert payload and salt_key to bytes
    payload_bytes = payload.encode('utf-8')
    salt_bytes = salt_key.encode('utf-8')
    
    # Insert salt at the salt index in the payload
    if salt_index > len(payload_bytes):
        salt_index = len(payload_bytes)  # Adjust if index is out of bounds
    
    salted_payload = payload_bytes[:salt_index] + salt_bytes + payload_bytes[salt_index:]
    
    # Base64 encode the salted payload
    base64_encoded = base64.b64encode(salted_payload)
    
    # Return the encoded string
    return base64_encoded.decode('utf-8')

def decode_with_salt(encoded_payload: str, salt_key: str, salt_index: int) -> str:
    # Decode the base64 string
    decoded_bytes = base64.b64decode(encoded_payload)
    
    # Convert salt_key to bytes
    salt_bytes = salt_key.encode('utf-8')
    
    # Extract the original payload by removing the salt at the correct index
    if decoded_bytes[salt_index:salt_index+len(salt_bytes)] == salt_bytes:
        # Remove the salt from the payload
        original_payload = decoded_bytes[:salt_index] + decoded_bytes[salt_index+len(salt_bytes):]
        return original_payload.decode('utf-8')
    else:
        raise ValueError("Invalid salt key or salt index")

# Example usage
payload = "Hello, this is a secret message!"
salt_key = "my_salt"
salt_index = 5

# Encode the payload
encoded_payload = encode_with_salt(payload, salt_key, salt_index)
print(f"Encoded Payload: {encoded_payload}")

# Decode the payload (with correct salt key and index)
try:
    decoded_payload = decode_with_salt(encoded_payload, salt_key, salt_index)
    print(f"Decoded Payload: {decoded_payload}")
except ValueError as e:
    print(e)

# Attempt to decode with incorrect salt key or index
try:
    decoded_payload = decode_with_salt(encoded_payload, "wrong_salt", salt_index)
    print(f"Decoded Payload with wrong salt: {decoded_payload}")
except ValueError as e:
    print(f"Decoding failed: {e}")
