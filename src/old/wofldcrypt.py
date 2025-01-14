
# The matching decryption script for woflcrypt:
# Simply fill in the msg, key and count hexes -
# Then run it and you're off!

# Function to convert plaintext to hexadecimal
def txt_to_hex(txt):
    return txt.encode('utf-8').hex().upper()

# Function to convert hexadecimal to plaintext, note "errs='ignore'" object!
def hex_to_txt(hex_str):
    return bytes.fromhex(hex_str).decode('utf-8', errors='ignore')

# Function to ensure key matches the length of the message by padding or truncating
def adjust_key_length(key, chr_val):
    if len(key) < chr_val:
        key = (key * ((chr_val // len(key)) + 1))[:chr_val]
    elif len(key) > chr_val:
        key = key[:chr_val]
    else:
        key = key  # This line is redundant but kept for clarity
    return key

# Function to XOR two hex strings after converting to integers
def xor_hex_strings(hex_key, hex_code):
    _key = int(hex_key, 16)
    _msg = int(hex_msg, 16)
    # # Perform XOR, convert result back to hex and make upper case:
    return hex(_key ^ _msg)[2:].upper().zfill(len(hex_key))  # Ensure it's the correct length

# Example code to decrypt, key as plaintext, character count as integer
hex_msg = "ENTER MSG HEX HERE"
hex_key = "ENTER KEY HEX HERE"
hex_cnt = "ENTER CNT HEX HERE"

# Convert hexadecimal character count to plaintext
chr_cnt = hex_to_txt(hex_cnt)  # Convert character count to string whilst converting from hex
txt_key = hex_to_txt(hex_key)

# convert hex value of cnt to integer for bitwise math
chr_val = int(chr_cnt, 16)
print(chr_val)

# Adjust key length to match the plaintext message
txt_key_ad= adjust_key_length(txt_key, chr_val)

# Print the results
print(f"Result for key=txt_key: {txt_key_ad}")

# Convert adjusted key to hexadecimal
hex_key_ad = txt_to_hex(txt_key_ad)

# Inline progress so far/useful err tracing
print(f"Encrypted message (hexadecimal): {hex_msg}")
print(f"Original message length (plaintext): {chr_val}")
print(f"Original Key (plaintext): {txt_key}")
print(f"Adjusted key (plaintext): {txt_key_ad}")
print(f"Original message (hexadecimal): {hex_msg}")
print(f"Adjusted key (hexadecimal): {hex_key_ad}")

# Decrypt the message by XORing the encrypted message with the key
dcrypt_hex = xor_hex_strings(hex_key, hex_msg)

# Output for final message
try:
    dcrypt_msg = hex_to_txt(dcrypt_hex)
    print(f"Decrypted message (hexadecimal): {dcrypt_hex}") # Print the decrypted message as hex
    print(f"Decrypted message (plaintext): {dcrypt_msg}") # Print the decrypted message as txt
# Since the decrypted message may not be valid UTF-8, handle it as a hex string
except UnicodeDecodeError:
    print(f"Decrypted message is not valid UTF-8. Decrypted message (hexadecimal): {dcrypt_hex}") # 
