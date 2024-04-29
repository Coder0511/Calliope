if __name__ == "__main__":
    from copy import deepcopy

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

    def state_from_bytes(data: bytes) -> [[int]]: # type: ignore
        return [data[i*4:(i+1)*4] for i in range(len(data) // 4)]

    def bytes_from_state(state: [[int]]) -> bytes: # type: ignore
        return bytes(state[0] + state[1] + state[2] + state[3])

    # NEW CONTENT HERE -------------------------------------------------------------------------------------------

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

    def inv_mix_rows(state: [[int]]): # type: ignore
        columns_to_rows(state)
        inv_mix_columns(state)
        rows_to_columns(state)

    expected_output = '63c9fe30f2f26326c9c97dd4fa6382d4'

    matrix = bytearray.fromhex('f82ebd0a26153dcf0d17fac271bd1811')
    matrix_bytes = state_from_bytes(matrix)

    inv_mix_rows(matrix_bytes)

    matrix_bytes = bytes_from_state(matrix_bytes)
    print(f'Test passed: {bytes.hex(matrix_bytes) == expected_output}')


    columns_to_rows_example = \
    """
    |63 c9 fe 30|           |63 f2 c9 fa|
    |f2 f2 63 26|  ------>  |c9 f2 c9 63|
    |c9 c9 7d d4|  ------>  |fe 63 7d 82|
    |fa 63 82 d4|           |30 26 d4 d4|
    """

    rows_to_columns_example = \
    """
    |63 f2 c9 fa|           |63 c9 fe 30|
    |c9 f2 c9 63|  ------>  |f2 f2 63 26|
    |fe 63 7d 82|  ------>  |c9 c9 7d d4|
    |30 26 d4 d4|           |fa 63 82 d4|
    """