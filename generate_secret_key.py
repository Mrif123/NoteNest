import os

# Generate a random byte string of 24 bytes
secret_key = os.urandom(24)

# Convert to a hexadecimal string for easier use
print("Your new secret key is:", secret_key.hex())
