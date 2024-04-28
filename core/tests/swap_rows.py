def state_from_bytes(data: bytes) -> [[int]]: # type: ignore
    return [data[i*4:(i+1)*4] for i in range(len(data) // 4)]

def bytes_from_state(state: [[int]]) -> bytes: # type: ignore
    return bytes(state[0] + state[1] + state[2] + state[3])

def swap_rows(state: [[int]]): # type: ignore
    state[0], state[1], state[2], state[3] = state[3], state[0], state[1], state[2]

expected_output = 'fa6382d463c9fe30f2f26326c9c97dd4'

matrix = bytearray.fromhex('63c9fe30f2f26326c9c97dd4fa6382d4')
matrix_bytes = state_from_bytes(matrix)

swap_rows(matrix_bytes)

matrix_bytes = bytes_from_state(matrix_bytes)
print(f'Test passed: {bytes.hex(matrix_bytes) == expected_output}')

example = \
"""
|63 c9 fe 30|           |fa 63 82 d4|
|f2 f2 63 26|  ------>  |63 c9 fe 30|
|c9 c9 7d d4|  ------>  |f2 f2 63 26|
|fa 63 82 d4|           |c9 c9 7d d4|
"""