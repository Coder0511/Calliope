from core.operations import operations

if __name__ == "__main__":
    plaintext = bytearray.fromhex("00112233445566778899aabbccddeeff")
    key = bytearray.fromhex('000102030405060708090a0b0c0d0e0f')
    # expected_ciphertext = bytearray.fromhex('69c4e0d86a7b0430d8cdb78070b4c55a')
    # ciphertext = operations.aes_encryption(plaintext, key)
    
    # print(ciphertext == expected_ciphertext)
    
    # deciphertext = operations.aes_decryption(ciphertext, key)
    
    # print(deciphertext == plaintext)
    
    calliope_ciphered = operations.calliope_static_encryption(plaintext, key)
    calliope_deciphered = operations.calliope_static_decryption(calliope_ciphered, key)
    print(calliope_deciphered == plaintext)