import typing as tp

def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    Encrypts plaintext using a Caesar cipher.

    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ""
    new_word = []
    for i in plaintext:
        if ord("A")<= i <= ord("Z"):
            ciphertext = chr((((ord(i) - 65) + shift) % 26) + 65)
            new_word.append(ciphertext)
        elif ord("a")<= i <= ord("z"):
            ciphertext = chr((((ord(i)- 97) + shift) % 26) + 97)
            new_word.append(ciphertext)
        else: 
            new_word.append(i)
    return ''.join(new_word)

def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    """
    Decrypts a ciphertext using a Caesar cipher.

    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ""
    new_word = []
    for i in ciphertext:
        if ord("A")<= i <= ord("Z"):
            plaintext = chr((((ord(i) - 65) - shift) % 26) + 65)
            new_word.append(plaintext)
        elif ord("a")<= i <= ord("z"):
            plaintext = chr((((ord(i) - 97) - shift) % 26) + 97)
            new_word.append(plaintext)
        else: 
            new_word.append(i)
    return ''.join(new_word)