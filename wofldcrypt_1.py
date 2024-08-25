# The matching decryption script for woflcrypt_adv:
# Fill in the msg, key and count, direction and rdn hexes -
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

# Decryption reverse shift with wrap function
def rot_hex(hex_msg, sht_amt, dir):
    # Convert hex string to an integer
    int_val = int(hex_msg, 16)
    
    # Get the number of bits in the integer
    bit_len = int_val.bit_length()
    
    if dir == 'right':
        # Perform the left rotation
        rot_val = (int_val << sht_amt) & (2**bit_len - 1)
        rot_val |= (int_val >> (bit_len - sht_amt))
    else:
        # Perform the right rotation otherwise
        rot_val = (int_val >> sht_amt) | ((int_val << (bit_len - sht_amt)) & (2**bit_len - 1))
    
    return rot_val

# Example code to decrypt, key as plaintext, character count as integer
hex_msg = "6161E000000000000000000"
hex_key = "454E544552204B4559205458542048455245E"
hex_rdn = "6C656646"
hex_dir = "6C656674"
hex_cnt = "3138"

# Decrypt the shift amount pair by XORing the direction & rdn pair
hex_rot = xor_hex_strings(hex_rdn, hex_dir)

# de-hex rotation/shift value
rot_val = hex_to_txt(hex_rot)

# Output for final message
try:
    dcryrpt_rdn = hex_to_txt(hex_rot)
    print(f"Decrypted rot val (hexadecimal): {hex_rot}") # Print the decrypted message as hex
    print(f"Decrypted rot val (plaintext): {rot_val}") # Print the decrypted message as txt
# Since the decrypted message may not be valid UTF-8, handle it as a hex string
except UnicodeDecodeError:
    print(f"Decrypted rot_val is not valid UTF-8. Decrypted rot val (hexadecimal): {hex_rot}")

# Convert hexadecimal character count, key, value and dir to plaintext
txt_cnt = hex_to_txt(hex_cnt)
txt_key = hex_to_txt(hex_key)
sht_dir = hex_to_txt(hex_dir)

# convert and/or write hex value of cnt and key to integer for bitwise math
chr_val = int(txt_cnt, 16)
print(chr_val)
int_key = int(txt_key, 16)
print(int_key)

# display direction
print(dir)

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
print(f"Rotation dir: {sht_dir}")
print(f"Rotation amount: {rot_val}")
print(f"Rotation direction (hexadecimal):{hex_dir}")
print(f"Rotation amount (hexadecimal): {hex_rot}")
print(f"Encrypted rotation amount vs. direction (hexadecimal): {hex_rdn}")

# reverse the shift using the defined function for opposite shift w/ wrap
# Calculate rotation display working rotated value
hex_msg = rot_hex(rot_val, sht_dir)
print(f"Rotated value (integer): {hex_msg}")

# Decrypt the message by XORing the encrypted message with the key
dcrypt_hex = xor_hex_strings(hex_key, hex_msg)

# Output for final message
try:
    dcrypt_msg = hex_to_txt(dcrypt_hex)
    print(f"Decrypted message (hexadecimal): {dcrypt_hex}") # Print the decrypted message as hex
    print(f"Decrypted message (plaintext): {dcrypt_msg}") # Print the decrypted message as txt
# Since the decrypted message may not be valid UTF-8, handle it as a hex string
except UnicodeDecodeError:
    print(f"Decrypted message is not valid UTF-8. Decrypted message (hexadecimal): {dcrypt_hex}")
