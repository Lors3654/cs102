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
        x = ord(i)
        if ord("A") <= x <= ord("Z"):
            ciphertext = chr((((x - ord("A")) + shift) % 26) + ord("A"))
            new_word.append(ciphertext)
        elif ord("a") <= x <= ord("z"):
            ciphertext = chr((((x - ord("a")) + shift) % 26) + ord("a"))
            new_word.append(ciphertext)
        else:
            new_word.append(i)
    return "".join(new_word)


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
        x = ord(i)
        if ord("A") <= x <= ord("Z"):
            plaintext = chr((((x - ord("A")) - shift) % 26) + ord("A"))
            new_word.append(plaintext)
        elif ord("a") <= x <= ord("z"):
            plaintext = chr((((x - ord("a")) - shift) % 26) + ord("a"))
            new_word.append(plaintext)
        else:
            new_word.append(i)
    return "".join(new_word)
