def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    ciphertext = ""
    len_alphabet = 26
    keyword_plus = [keyword[index % len(keyword)] for index in range(len(plaintext))]
    for index, symbol in enumerate(plaintext):
        up_low = ord("A") if symbol.isupper() else ord("a")
        symbol = plaintext[index]
        if symbol.isalpha():
            ciphertext += chr((ord(symbol) + (ord(keyword_plus[index]) % up_low) - up_low) % len_alphabet + up_low)
        else:
            ciphertext += symbol
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    plaintext = ""
    len_alphabet = 26
    keyword_plus = [keyword[i % len(keyword)] for i in range(len(ciphertext))]
    for index, symbol in enumerate(ciphertext):
        up_low = ord("A") if symbol.isupper() else ord("a")
        symbol = ciphertext[index]
        if symbol.isalpha():
            plaintext += chr((ord(symbol) - (ord(keyword_plus[index]) % up_low) - up_low) % len_alphabet + up_low)
        else:
            plaintext += symbol
    return plaintext