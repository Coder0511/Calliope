if __name__ == "__main__":    
    def state_from_bytes(data: bytes) -> [[int]]: # type: ignore
        return [data[i*4:(i+1)*4] for i in range(len(data) // 4)]

    def bytes_from_state(state: [[int]]) -> bytes: # type: ignore
        return bytes(state[0] + state[1] + state[2] + state[3])

    def shift_columns(state: [[int]]): # type: ignore
        state[0][1], state[1][1], state[2][1], state[3][1] = state[3][1], state[0][1], state[1][1], state[2][1]
        state[0][2], state[1][2], state[2][2], state[3][2] = state[2][2], state[3][2], state[0][2], state[1][2]
        state[0][3], state[1][3], state[2][3], state[3][3] = state[1][3], state[2][3], state[3][3], state[0][3]

    expected_output = '63637d26f2c982d4c9f2fed4fac96330'

    matrix = bytearray.fromhex('63c9fe30f2f26326c9c97dd4fa6382d4')
    matrix_bytes = state_from_bytes(matrix)

    shift_columns(matrix_bytes)

    matrix_bytes = bytes_from_state(matrix_bytes)
    print(f'Test passed: {bytes.hex(matrix_bytes) == expected_output}')
        
    example = \
    """
    |63 c9 fe 30|           |63 63 7d 26|
    |f2 f2 63 26|  ------>  |f2 c9 82 d4|
    |c9 c9 7d d4|  ------>  |c9 f2 fe d4|
    |fa 63 82 d4|           |fa c9 63 30|
    """