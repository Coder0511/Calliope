from .sub_byte_strings import sub_byte_box_string, inv_sub_byte_box_string, s_box, inv_s_box

def state_from_bytes(data: bytes) -> [[int]]: # type: ignore
    state = [data[i*4:(i+1)*4] for i in range(len(data) // 4)]
    return state

def rotate_word(word: [int]) -> [int]: # type: ignore
    return word[1:] + word[:1]

def substitution_word(word: [int]) -> bytes: # type: ignore
    substituted_word = bytes(s_box[i] for i in word)
    return substituted_word

def round_constant(i: int) -> bytes:
    round_constant_lookup = bytearray.fromhex('01020408102040801B36')
    round_constant_value = bytes([round_constant_lookup[i-1], 0, 0, 0])
    return round_constant_value

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

def bytes_from_state(state: [[int]]) -> bytes: # type: ignore
    cipher = bytes(state[0] + state[1] + state[2] + state[3])
    return cipher

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
    
    cipher = bytes_from_state(state)
    return cipher
