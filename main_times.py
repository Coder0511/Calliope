if __name__ == "__main__":
    from core.operations import operations
    import time
    
    plaintext = bytearray.fromhex("00112233445566778899aabbccddeeff")
    key = bytearray.fromhex('000102030405060708090a0b0c0d0e0f')
    
    start = time.time()
    aes_ciphered = operations.aes_encryption(plaintext, key)
    aes_deciphered = operations.aes_decryption(aes_ciphered, key)
    end = time.time()
    print(f"AES test passed: {aes_deciphered == plaintext}")
    print(f"Time: {end-start} seconds\n")
    
    start = time.time()
    calliope_ciphered_static = operations.calliope_static_encryption(plaintext, key)
    calliope_deciphered_static = operations.calliope_static_decryption(calliope_ciphered_static, key)
    end = time.time()
    print(f"Calliope static test passed: {calliope_deciphered_static == plaintext}")
    print(f"Time: {end-start} seconds\n")
    
    start = time.time()
    calliope_ciphered_random = operations.calliope_random_encryption(plaintext, key, [2, 2])
    calliope_deciphered_random = operations.calliope_random_decryption(calliope_ciphered_random, key, [4, 2])
    end = time.time()
    print(f"Calliope random test passed: {calliope_deciphered_random == plaintext}")
    print(f"Time: {end-start} seconds")