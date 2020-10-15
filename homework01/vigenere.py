def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.

    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    while len(plaintext) > len(keyword):
        keyword += keyword
    for i in range(len(plaintext)):
        x = plaintext[i]
        y = keyword[i % len(keyword)]
        if 'A' <= x <= 'Z':
            code = ord(x) + ord(y) - ord("A")
            if (code > ord('Z')):
                code = code - 26
        else:
            code = ord(x) + ord(y) - ord("a")
            if (code > ord('z')):
                code = code - 26
        ciphertext += chr(code)
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.

    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    while len(plaintext) > len(keyword):
        keyword += keyword
    for i in range(len(ciphertext)):
        x = ciphertext[i]
        y = keyword[i % len(keyword)]
        if 'A' <= x <= 'Z':
            code = ord(x) - ord(y) + ord("A")
            if (code < ord('A')):
                code = code + 26
        else:
            code = ord(x) - ord(y) + ord("a")
            if (code < ord('a')):
                code = code + 26
        plaintext += chr(code)
    return plaintext