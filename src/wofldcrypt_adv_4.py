# The matching decryption script for woflcrypt_adv:
# Fill in the msg, key, count, direction, and rdn hexes -
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
    return key

# Function to XOR two hex strings after converting to integers
def xor_hex_strings(hex_key, hex_code):
    _key = int(hex_key, 16)
    _msg = int(hex_code, 16)
    # Perform XOR, convert result back to hex and make upper case:
    return hex(_key ^ _msg)[2:].upper().zfill(len(hex_key))  # Ensure it's the correct length

# Decryption reverse shift with wrap function
def rot_hex(hex_msg, sht_amt, direction='left'):
    # Convert hex string to an integer
    int_val = int(hex_msg, 16)
    
    # Get the number of bits in the integer
    bit_len = int_val.bit_length()
    
    if direction == 'right':
        # Perform the right rotation
        rot_val = (int_val >> sht_amt) | ((int_val << (bit_len - sht_amt)) & (2**bit_len - 1))
    else:
        # Perform the left rotation otherwise
        rot_val = (int_val << sht_amt) & (2**bit_len - 1)
        rot_val |= (int_val >> (bit_len - sht_amt))
    
    return rot_val

# Example code to decrypt, key as plaintext, character count as integer
hex_msg = "6161E000000000000000000"
hex_key = "454E544552204B4559205458542048455245"
hex_rdn = "6C656646"
hex_dir = "6C656674"
hex_cnt = "3138"
hex_rdr = "31"

# Convert hexadecimal character count, rdn count, rdn and key to plaintext
txt_cnt = hex_to_txt(hex_cnt)
txt_key = hex_to_txt(hex_key)
rdr_cnt = hex_to_txt(hex_rdr)
rdn = hex_to_txt(hex_rdn)

# Convert character count to integer
chr_val = int(txt_cnt)

# Covert rdn count to integer
rdn = int(rdr_cnt)

# Adjust key length to match the plaintext message
txt_key_ad = adjust_key_length(txt_key, chr_val)

# Funtion to ensure rotation matches the legth of the message by padding or trunctating
def adjust_rdn_Length(rdn, cnt_rdr):    
    if len(rdn) < cnt_rdr:
        rdn + (dir * ((cnt_rdr // len(rdn)) + 1))[:cnt_rdr]
    elif len(rdn) > cnt_rdr:
            rdn = dir[:cnt_rdr]
    return rdn

# convert hexcode rdn to plaintext integer rdn
cnt_rdr = hex_to_txt(hex_rdr)

# Adjust rdn length to match the length of plaintxt rdn integer
rdn_adj = adjust_rdn_length(rdn, cnt_rdr) 

# Convert adjusted key and rdn to hexadecimal
hex_key_ad = txt_to_hex(txt_key_ad)
hex_rdn_ad = txt_to_hex(rdn_adj)

# Decrypt the shift amount pair by XORing the direction & rdn pair
hex_rot = xor_hex_strings(hex_rdn_ad, hex_dir)

# Output for final message
try:

# Convert rotation/shift value from hex to integer
rot_val = int(hex_rot, 16)

print(f"Decrypted rot val (hexadecimal): {hex_rot}") # Print the decrypted message as hex
print(f"Decrypted rot val (integer): {rot_val}") # Print the decrypted message as int
# Since the decrypted message may not be valid UTF-8, handle it as a hex string
except UnicodeDecodeError:
print(f"Decrypted rot_val is not valid UTF-8. Decrypted rot val (hexadecimal): {hex_rot}")

# Inline progress so far/useful error tracing
print(f"Encrypted message (hexadecimal): {hex_msg}")
print(f"Original message length (plaintext): {chr_val}")
print(f"Original Key (plaintext): {txt_key}")
print(f"Adjusted key (plaintext): {txt_key_ad}")
print(f"Original message (hexadecimal): {hex_msg}")
print(f"Adjusted key (hexadecimal): {hex_key_ad}")
print(f"Rotation direction (hexadecimal): {hex_dir}")
print(f"Rotation amount (hexadecimal): {hex_rot}")
print(f"Encrypted rotation amount vs. direction (hexadecimal): {hex_rdn}")
print(f"Adjusted RDN: {rdn_adj}, Adjusted RDN (headecimal: {hex_rdn_ad})")

# Determine the rotation direction
sht_dir = hex_to_txt(hex_dir).lower()
direction = 'right' if sht_dir == 'right' else 'left'

# Reverse the shift using the defined function for opposite shift with wrap
# Calculate rotation and display working rotated value
rotated_val = rot_hex(hex_msg, rot_val, direction=direction)
hex_rotated = hex(rotated_val)[2:].upper().zfill(len(hex_msg))

# Decrypt the message by XORing the encrypted message with the key
dcrypt_hex = xor_hex_strings(hex_key_ad, hex_rotated)

# Output for final message
try:
    dcrypt_msg = hex_to_txt(dcrypt_hex)
    print(f"Decrypted message (hexadecimal): {dcrypt_hex}") # Print the decrypted message as hex
    print(f"Decrypted message (plaintext): {dcrypt_msg}") # Print the decrypted message as txt
# Since the decrypted message may not be valid UTF-8, handle it as a hex string
except UnicodeDecodeError:
    print(f"Decrypted message is not valid UTF-8. Decrypted message (hexadecimal): {dcrypt_hex}")
