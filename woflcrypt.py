# wofl's next encryption script: converts plaintxt
# to encrypted hexcode via a key (also hexcode output) -
# Needs the hexcode char count to decrypt too!
# this one rotates the hex msg a given amount before xor

# Function to convert plaintext to hexadecimal
def txt_to_hex(txt):
    return txt.encode('utf-8').hex().upper()

# Function to count the characters in the plaintext message
def cnt_chrs(txt_msg):
    return len(txt_msg)

def rot_hex(hex_msg, sht_amt, dir):
    # Convert hex string to an integer
    int_val = int(hex_msg, 16)
    
    # Get the number of bits in the integer
    bit_len = int_val.bit_length()
    
    if dir == 'left':
        # Perform the left rotation
        rot_val = (int_val << sht_amt) & (2**bit_len - 1)
        rot_val |= (int_val >> (bit_len - sht_amt))
    else:
        # Perform the right rotation otherwise
        rot_val = (int_val >> sht_amt) | ((int_val << (bit_len - sht_amt)) & (2**bit_len - 1))
    
    return rot_val

# Example plaintext strings
txt_msg = "ENTER MSG TXT HERE"
txt_key = "ENTER KEY TXT HERE"
sht_amt = 2 # Be sure to replace with desired shift amount as an integer, no " ' "
dir = 'left' # Be sure to replace with lc 'left' or 'right' only!
char_cnt = cnt_chrs(txt_msg)

# Convert plaintext to hexadecimal
hex_msg = txt_to_hex(txt_msg)
hex_key = txt_to_hex(txt_key)
hex_cnt = txt_to_hex(str(char_cnt))  # Convert character count to string before converting to hex

# Calculate rotation display working rotated value
rot_val = rot_hex(hex_msg, sht_amt, dir)
print(f"rotated value (integer): {rot_val}")
print(f"Rotation direction: {dir}")

# Convert the rotation result back to hex and display
hex_rot = hex(rot_val)[2:]  # Removing '0x' prefix
print(f"rotated value (hexadecimal): {hex_rot}")
hex_dir = txt_to_hex(dir)
print(f"Rotation direction (hexadecimal): {hex_dir}")

# Convert hexadecimal strings to integers
_msg = rot_val
_key = int(hex_key, 16)

# Perform XOR operation
cryptd = _msg ^ _key

# Convert the result back to hexadecimal by removing '0x' prefix and 
hex_cptd = hex(cryptd)[2:].upper()

# Print results
print(f"Message text: {txt_msg}")
print(f"Original message (hexadecimal): {hex_msg}")
print(f"Encoded message (hexadecimal & encrypted): {hex_cptd}")
print(f"Key plaintext: {txt_key}, Key hex: {hex_key}")
print(f"Char count: {char_cnt}, Char count (hexadecimal): {hex_cnt}")
