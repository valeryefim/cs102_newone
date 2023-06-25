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
    original_word = str(plaintext)
    if len(original_word) != 0:
        for letter in original_word:
            if letter.isalpha():
                if letter.isupper():
                    encrypted_letter = chr((ord(letter) - ord("A") + shift) % 26 + ord("A"))
                else:
                    encrypted_letter = chr((ord(letter) - ord("a") + shift) % 26 + ord("a"))
                ciphertext += encrypted_letter
            else:
                ciphertext += letter
    return ciphertext


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
    original_word = str(ciphertext)
    if len(original_word) != 0:
        for letter in original_word:
            if letter.isalpha():
                if letter.isupper():
                    decrypted_letter = chr((ord(letter) - ord("A") - shift) % 26 + ord("A"))
                else:
                    decrypted_letter = chr((ord(letter) - ord("a") - shift) % 26 + ord("a"))
                plaintext += decrypted_letter
            else:
                plaintext += letter
    return plaintext


if __name__ == "__main__":
    print(decrypt_caesar("sbwkrq"))
