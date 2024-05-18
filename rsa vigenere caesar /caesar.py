def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    len_alphabet = 26
    encrypted = ""
    for symbol in plaintext:
        up_low = ord("A") if symbol.isupper() else ord("a")
        if symbol.isalpha():
            encrypted += chr((ord(symbol) - up_low + shift) % len_alphabet + up_low)
        else:
            encrypted += symbol
    return encrypted


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    plaintext = ""
    len_alphabet = 26
    for symbol in ciphertext:
        up_low = ord("A") if symbol.isupper() else ord("a")
        if symbol.isalpha():
            plaintext += chr((ord(symbol) - up_low - shift) % len_alphabet + up_low)
        else:
            plaintext += symbol
    return plaintext