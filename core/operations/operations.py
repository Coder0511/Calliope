import time
from copy import deepcopy
from .sub_byte_strings import s_box, inv_s_box

# Key operations ---------------------------------------------------------------------------------

def state_from_bytes(data: bytes) -> [[int]]: # type: ignore
    return [data[i*4:(i+1)*4] for i in range(len(data) // 4)]

def bytes_from_state(state: [[int]]) -> bytes: # type: ignore
    return bytes(state[0] + state[1] + state[2] + state[3])

def rotate_word(word: [int]) -> [int]: # type: ignore
    return word[1:] + word[:1]

def substitution_word(word: [int]) -> bytes: # type: ignore
    return bytes(s_box[i] for i in word)

def round_constant(i: int) -> bytes:
    round_constant_lookup = bytearray.fromhex('01020408102040801B36')
    return bytes([round_constant_lookup[i-1], 0, 0, 0])

def xor_bytes(a: bytes, b:bytes):
    return bytes([x ^ y for(x, y) in zip(a, b)])
    

def key_expansion(key: bytes, bytes_number: int = 4) -> [[[int]]]: # type: ignore
    keys_number = len(key) // 4
    rounds = 10
    word = state_from_bytes(key)
    
    for i in range(keys_number, bytes_number * (rounds + 1)):
        temp = word[i-1]
        if i % keys_number == 0:
            temp = xor_bytes(substitution_word(rotate_word(temp)), round_constant(i//keys_number))
        elif keys_number > 6 and i % keys_number == 4:
            temp = substitution_word(temp)
        word.append(xor_bytes(word[i-keys_number], temp))
    
    return [word[i*4:(i+1)*4] for i in range(len(word)//4)]

def add_round_key(state: [[int]], key_schedule: [[int]], round: int): # type: ignore
    round_key = key_schedule[round]
    for row in range(len(state)):
        state[row] = [state[row][column] ^ round_key[row][column] for column in range(len(state[0]))]
        
# AES Encryption operations ---------------------------------------------------------------------------------

def sub_bytes(state: [[int]]): # type: ignore
    for row in range(len(state)):
        state[row] = [s_box[state[row][column]] for column in range(len(state[0]))]

def shift_rows(state: [[int]]): # type: ignore
    state[0][1], state[1][1], state[2][1], state[3][1] = state[1][1], state[2][1], state[3][1], state[0][1]
    state[0][2], state[1][2], state[2][2], state[3][2] = state[2][2], state[3][2], state[0][2], state[1][2]
    state[0][3], state[1][3], state[2][3], state[3][3] = state[3][3], state[0][3], state[1][3], state[2][3]

def xtime(a: int) -> int:
    if a & 0x80:
        return ((a<<1) ^ 0x1b) & 0xff
    return a << 1

def mix_column(column: [int]): # type: ignore
    column0 = column[0]
    all_xor = column[0] ^ column[1] ^ column[2] ^ column[3]
    
    column[0] ^= xtime(column[0] ^ column[1]) ^ all_xor
    column[1] ^= xtime(column[1] ^ column[2]) ^ all_xor
    column[2] ^= xtime(column[2] ^ column[3]) ^ all_xor
    column[3] ^= xtime(column0 ^ column[3]) ^ all_xor

def mix_columns(state: [[int]]): # type: ignore
    for row in state:
        mix_column(row)

# AES Encryption ---------------------------------------------------------------------------------

def aes_encryption(data: bytes, key: bytes) -> bytes:
    state = state_from_bytes(data)
    key_schedule = key_expansion(key)
    add_round_key(state, key_schedule, round=0)
    
    rounds = 10
    
    for round in range (1, rounds):
        sub_bytes(state)
        shift_rows(state)
        mix_columns(state)
        add_round_key(state, key_schedule, round)
        
    sub_bytes(state)
    shift_rows(state)
    add_round_key(state, key_schedule, round=rounds)
    
    return bytes_from_state(state)

# AES Decryption operations ---------------------------------------------------------------------------------

def inv_sub_bytes(state: [[int]]): # type: ignore
    for row in range(len(state)):
        state[row] = [inv_s_box[state[row][column]] for column in range(len(state[0]))]
        
def inv_shift_rows(state: [[int]]): # type: ignore
    state[1][1], state[2][1], state[3][1], state[0][1] = state[0][1], state[1][1], state[2][1], state[3][1]
    state[2][2], state[3][2], state[0][2], state[1][2] = state[0][2], state[1][2], state[2][2], state[3][2]
    state[3][3], state[0][3], state[1][3], state[2][3] = state[0][3], state[1][3], state[2][3], state[3][3]
    
def xtimes_0e(b):
    return xtime(xtime(xtime(b) ^ b) ^ b)


def xtimes_0b(b):
    return xtime(xtime(xtime(b)) ^ b) ^ b


def xtimes_0d(b):
    return xtime(xtime(xtime(b) ^ b)) ^ b


def xtimes_09(b):
    return xtime(xtime(xtime(b))) ^ b

def inv_mix_column(col: [int]): # type: ignore
    u = xtime(xtime(col[0] ^ col[2]))
    v = xtime(xtime(col[1] ^ col[3]))
    col[0] ^= u
    col[1] ^= v
    col[2] ^= u
    col[3] ^= v


def inv_mix_columns(state: [[int]]) -> [[int]]: # type: ignore
    for row in state:
        inv_mix_column(row)
    mix_columns(state)

# AES Decryption ---------------------------------------------------------------------------------

def aes_decryption(cipher: bytes, key: bytes) -> bytes:
    rounds = 10

    state = state_from_bytes(cipher)
    key_schedule = key_expansion(key)
    add_round_key(state, key_schedule, round=rounds)

    for round in range(rounds-1, 0, -1):
        inv_shift_rows(state)
        inv_sub_bytes(state)
        add_round_key(state, key_schedule, round)
        inv_mix_columns(state)

    inv_shift_rows(state)
    inv_sub_bytes(state)
    add_round_key(state, key_schedule, round=0)

    return bytes_from_state(state)

# Calliope encryption operations ---------------------------------------------------------------------------------

def shift_columns(state: [[int]]): # type: ignore
    state[0][1], state[1][1], state[2][1], state[3][1] = state[3][1], state[0][1], state[1][1], state[2][1]
    state[0][2], state[1][2], state[2][2], state[3][2] = state[2][2], state[3][2], state[0][2], state[1][2]
    state[0][3], state[1][3], state[2][3], state[3][3] = state[1][3], state[2][3], state[3][3], state[0][3]
    
def swap_columns(state: [[int]]): # type: ignore
    state[0][0], state[0][1], state[0][2], state[0][3] = state[0][3], state[0][0], state[0][1], state[0][2]
    state[1][0], state[1][1], state[1][2], state[1][3] = state[1][3], state[1][0], state[1][1], state[1][2]
    state[2][0], state[2][1], state[2][2], state[2][3] = state[2][3], state[2][0], state[2][1], state[2][2]
    state[3][0], state[3][1], state[3][2], state[3][3] = state[3][3], state[3][0], state[3][1], state[3][2]
    
def swap_rows(state: [[int]]): # type: ignore
    state[0], state[1], state[2], state[3] = state[3], state[0], state[1], state[2]
    
def columns_to_rows(state: [[int]]): # type: ignore
    temporal_list = deepcopy(state)
    state[0][0], state[0][1], state[0][2], state[0][3] = temporal_list[0][0], temporal_list[1][0], temporal_list[2][0], temporal_list[3][0]
    state[1][0], state[1][1], state[1][2], state[1][3] = temporal_list[0][1], temporal_list[1][1], temporal_list[2][1], temporal_list[3][1]
    state[2][0], state[2][1], state[2][2], state[2][3] = temporal_list[0][2], temporal_list[1][2], temporal_list[2][2], temporal_list[3][2]
    state[3][0], state[3][1], state[3][2], state[3][3] = temporal_list[0][3], temporal_list[1][3], temporal_list[2][3], temporal_list[3][3]

def rows_to_columns(state: [[int]]): # type: ignore
    temporal_list = deepcopy(state)
    state[0][0], state[1][0], state[2][0], state[3][0] = temporal_list[0][0], temporal_list[0][1], temporal_list[0][2], temporal_list[0][3]
    state[0][1], state[1][1], state[2][1], state[3][1] = temporal_list[1][0], temporal_list[1][1], temporal_list[1][2], temporal_list[1][3]
    state[0][2], state[1][2], state[2][2], state[3][2] = temporal_list[2][0], temporal_list[2][1], temporal_list[2][2], temporal_list[2][3]
    state[0][3], state[1][3], state[2][3], state[3][3] = temporal_list[3][0], temporal_list[3][1], temporal_list[3][2], temporal_list[3][3]

def mix_rows(state: [[int]]): # type: ignore
    columns_to_rows(state)
    mix_columns(state)
    rows_to_columns(state)

# Calliope decryption operations ---------------------------------------------------------------------------------

def inv_shift_columns(state: [[int]]): # type: ignore
    state[3][1], state[0][1], state[1][1], state[2][1] = state[0][1], state[1][1], state[2][1], state[3][1]
    state[2][2], state[3][2], state[0][2], state[1][2] = state[0][2], state[1][2], state[2][2], state[3][2]
    state[1][3], state[2][3], state[3][3], state[0][3] = state[0][3], state[1][3], state[2][3], state[3][3]
    
def inv_swap_columns(state: [[int]]): # type: ignore
    state[0][3], state[0][0], state[0][1], state[0][2] = state[0][0], state[0][1], state[0][2], state[0][3]
    state[1][3], state[1][0], state[1][1], state[1][2] = state[1][0], state[1][1], state[1][2], state[1][3]
    state[2][3], state[2][0], state[2][1], state[2][2] = state[2][0], state[2][1], state[2][2], state[2][3]
    state[3][3], state[3][0], state[3][1], state[3][2] = state[3][0], state[3][1], state[3][2], state[3][3]
    
def inv_swap_rows(state: [[int]]): # type: ignore
    state[3], state[0], state[1], state[2] = state[0], state[1], state[2], state[3]
    
def inv_mix_rows(state: [[int]]): # type: ignore
    columns_to_rows(state)
    inv_mix_columns(state)
    rows_to_columns(state)
    
# Calliope static encryption ---------------------------------------------------------------------------------

def calliope_static_encryption(data: bytes, key: bytes) -> bytes:
    state = state_from_bytes(data)
    key_schedule = key_expansion(key)
    add_round_key(state, key_schedule, round=0)
    
    rounds = 10
    
    for round in range (1, rounds):
        sub_bytes(state)
        shift_rows(state)
        shift_columns(state)
        swap_rows(state)
        swap_columns(state)
        mix_rows(state)
        mix_columns(state)
        add_round_key(state, key_schedule, round)
        
    sub_bytes(state)
    shift_rows(state)
    shift_columns(state)
    swap_rows(state)
    swap_columns(state)
    add_round_key(state, key_schedule, round=rounds)
    
    return bytes_from_state(state)

# Calliope static decryption ---------------------------------------------------------------------------------

def calliope_static_decryption(cipher: bytes, key: bytes) -> bytes:
    rounds = 10

    state = state_from_bytes(cipher)
    key_schedule = key_expansion(key)
    add_round_key(state, key_schedule, round=rounds)

    for round in range(rounds-1, 0, -1):
        inv_swap_columns(state)
        inv_swap_rows(state)
        inv_shift_columns(state)
        inv_shift_rows(state)
        inv_sub_bytes(state)
        add_round_key(state, key_schedule, round)
        inv_mix_columns(state)
        inv_mix_rows(state)

    inv_swap_columns(state)
    inv_swap_rows(state)
    inv_shift_columns(state)
    inv_shift_rows(state)
    inv_sub_bytes(state)
    add_round_key(state, key_schedule, round=0)

    return bytes_from_state(state)

# Calliope random encryption ---------------------------------------------------------------------------------

def get_x_operation(value: int):
    if value == 1:
        return 'shift_rows'
    elif value == 2:
        return 'swap_rows'
    elif value == 3:
        return 'shift_columns'
    return 'swap_columns'
def get_y_operation(value: int):
    if value == 1:
        return 'mix_columns'
    return 'mix_rows'

def calliope_random_encryption(data: bytes, key: bytes, selected: [int]) -> bytes: # type: ignore
    state = state_from_bytes(data)
    key_schedule = key_expansion(key)
    add_round_key(state, key_schedule, round=0)
    
    rounds = 10
    
    x_string = get_x_operation([selected[0]])
    y_string = get_y_operation([selected[1]])
    
    for round in range (1, rounds):
        sub_bytes(state)
        globals()[x_string](state)
        globals()[y_string](state)
        add_round_key(state, key_schedule, round)
        
    sub_bytes(state)
    globals()[x_string](state)
    add_round_key(state, key_schedule, round=rounds)
    
    return bytes_from_state(state)

# Calliope random decryption ---------------------------------------------------------------------------------

def get_inv_x_operation(value: int):
    if value == 1:
        return 'inv_shift_rows'
    elif value == 2:
        return 'inv_swap_rows'
    elif value == 3:
        return 'inv_shift_columns'
    return 'inv_swap_columns'
def get_inv_y_operation(value: int):
    if value == 1:
        return 'inv_mix_columns'
    return 'inv_mix_rows'

def calliope_random_decryption(cipher: bytes, key: bytes, selected: [int]) -> bytes: # type: ignore
    rounds = 10

    state = state_from_bytes(cipher)
    key_schedule = key_expansion(key)
    add_round_key(state, key_schedule, round=rounds)
    
    inv_x_string = get_inv_x_operation([selected[0]])
    inv_y_string = get_inv_y_operation([selected[1]])

    for round in range(rounds-1, 0, -1):
        globals()[inv_x_string](state)
        inv_sub_bytes(state)
        add_round_key(state, key_schedule, round)
        globals()[inv_y_string](state)

    globals()[inv_x_string](state)
    inv_sub_bytes(state)
    add_round_key(state, key_schedule, round=0)

    return bytes_from_state(state)

# Get text and process it ---------------------------------------------------------------------------------

# def pkcs7_encode(text):
#     pkcs7 = PKCS7Encoder(16)
#     return pkcs7.encode(text)

def clean_string(text: str):
    text = text.encode().hex()
    return f"{text}"

def execute_calliope_encrypt(message, algorithm, x_operation, y_operation, key):
    if algorithm == 1:
        return calliope_random_encryption(message, key, [x_operation, y_operation])
    return calliope_static_encryption(message, key)

def execute_calliope_decrypt(message, algorithm, x_operation, y_operation, key):
    if algorithm == 1:
        return calliope_random_decryption(message, key, [x_operation, y_operation])
    return calliope_static_decryption(message, key)

def save_file(path, lines):
    with open(path, 'w') as file:
        for line in lines:
            file.write(line)

def process_string(process, algorithm, message, key):
    if process == "encriptar":
        message = bytearray.fromhex(clean_string(message))
        if algorithm == "aes":
            key = bytearray.fromhex(key[0:-6])
            return bytes.hex(aes_encryption(message, key))
        
        algorithm_int = int(key[-6:-4])
        x_operation = int(key[-4:-2])
        y_operation = int(key[-2:])
        key = bytearray.fromhex(key[0:-6])
        return bytes.hex(execute_calliope_encrypt(message, algorithm_int, x_operation, y_operation, key))
    
    message = bytearray.fromhex(message)
    if algorithm == "aes":
        key = bytearray.fromhex(key[0:-6])
        return aes_decryption(message, key).decode("utf-8")
    
    algorithm_int = int(key[-6:-4])
    x_operation = int(key[-4:-2])
    y_operation = int(key[-2:])
    key = bytearray.fromhex(key[0:-6])
    return execute_calliope_decrypt(message, algorithm_int, x_operation, y_operation, key).decode("utf-8")

def process_file(file_path, process, algorithm, key, save_path):
    try:    
        text = open(file_path, "r").read()
        name = (file_path.split("\\")[-1])[:-4]
        path = f"{save_path}\\{name}-encrypted.txt" if (process=="encriptar") else f"{save_path}\\{name}-decrypted.txt"

        start = time.time()
        if process == "encriptar":
            text = [text[i:i+16] for i in range(0, len(text), 16)]
            for i in range(0, len(text)):
                text[i] = bytearray.fromhex(clean_string(text[i]))
            if algorithm == "aes":
                key = bytearray.fromhex(key[0:-6])
                for i in range(0, len(text)):
                    text[i] = bytes.hex(aes_encryption(text[i], key))
                end = time.time()
                print(end-start)
                return save_file(path, text)
            
            algorithm_int = int(key[-6:-4])
            x_operation = int(key[-4:-2])
            y_operation = int(key[-2:])
            key = bytearray.fromhex(key[0:-6])
            for i in range(0, len(text)):
                text[i] = bytes.hex(execute_calliope_encrypt(text[i], algorithm_int, x_operation, y_operation, key))
            end = time.time()
            print(end-start)
            return save_file(path, text)
        
        text = [text[i:i+32] for i in range(0, len(text), 32)]
        for i in range(0, len(text)):
            text[i] = bytearray.fromhex(text[i])
        if algorithm == "aes":
            key = bytearray.fromhex(key[0:-6])
            for i in range(0, len(text)):
                text[i] = aes_decryption(text[i], key).decode("utf-8")
            end = time.time()
            print(end-start)
            return save_file(path, text)
        
        algorithm_int = int(key[-6:-4])
        x_operation = int(key[-4:-2])
        y_operation = int(key[-2:])
        key = bytearray.fromhex(key[0:-6])
        for i in range(0, len(text)):
            text[i] = execute_calliope_decrypt(text[i], algorithm_int, x_operation, y_operation, key).decode("utf-8")
        end = time.time()
        print(end-start)
        return save_file(path, text)
    except:
        return None