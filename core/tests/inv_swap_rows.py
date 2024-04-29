if __name__ == "__main__":    
    def state_from_bytes(data: bytes) -> [[int]]: # type: ignore
        return [data[i*4:(i+1)*4] for i in range(len(data) // 4)]

    def bytes_from_state(state: [[int]]) -> bytes: # type: ignore
        return bytes(state[0] + state[1] + state[2] + state[3])

    def inv_swap_rows(state: [[int]]): # type: ignore
        state[3], state[0], state[1], state[2] = state[0], state[1], state[2], state[3]

    expected_output = '63c9fe30f2f26326c9c97dd4fa6382d4'

    matrix = bytearray.fromhex('fa6382d463c9fe30f2f26326c9c97dd4')
    matrix_bytes = state_from_bytes(matrix)

    inv_swap_rows(matrix_bytes)

    matrix_bytes = bytes_from_state(matrix_bytes)
    print(f'Test passed: {bytes.hex(matrix_bytes) == expected_output}')

    example = \
    """
    |fa 63 82 d4|           |63 c9 fe 30|
    |63 c9 fe 30|  ------>  |f2 f2 63 26|
    |f2 f2 63 26|  ------>  |c9 c9 7d d4|
    |c9 c9 7d d4|           |fa 63 82 d4|
    """