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
    for i in range (len(plaintext)):
        x = i % len(keyword)
        y = keyword[x]
        z = plaintext[i]
        if 'A' <= z <= 'Z':
            key = ord(y) - ord("A")
            code = chr((ord(z) - ord("A") + key) % 26 + ord("A"))
        elif 'a' <= z <= 'z':
            key = ord(y) - ord("a")
            code = chr((ord(z) - ord("a") + key) % 26 + ord("a"))
        else: code = z
        ciphertext = ciphertext + code
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
    for i in range (len(ciphertext)):
        x = i % len(keyword)
        y = keyword[x]
        z = ciphertext[i]
        if 'A' <= z <= 'Z':
            key = ord(y) - ord("A")
            code = chr((ord(z) - ord("A") - key) % 26 + ord("A"))
        elif 'a' <= z <= 'z':
            key = ord(y) - ord("a")
            code = chr((ord(z) - ord("a") - key) % 26 + ord("a"))
        else: code = z
        plaintext = plaintext + code
    return plaintext