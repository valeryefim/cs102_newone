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
    encrypted_text = ""
    keyword = keyword.upper()
    keyword_length = len(keyword)
    for i, char in enumerate(plaintext):
        if char.isalpha():
            shift = ord(keyword[i % keyword_length]) - ord("A")
            if char.isupper():
                encrypted_char = chr((ord(char) - ord("A") + shift) % 26 + ord("A"))
            else:
                encrypted_char = chr((ord(char) - ord("a") + shift) % 26 + ord("a"))
            encrypted_text += encrypted_char
        else:
            encrypted_text += char
    return encrypted_text


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
    decrypted_text = ""
    keyword = keyword.upper()
    keyword_length = len(keyword)
    for i, char in enumerate(ciphertext):
        if char.isalpha():
            shift = ord(keyword[i % keyword_length]) - ord("A")
            if char.isupper():
                decrypted_char = chr((ord(char) - ord("A") - shift) % 26 + ord("A"))
            else:
                decrypted_char = chr((ord(char) - ord("a") - shift) % 26 + ord("a"))
            decrypted_text += decrypted_char
        else:
            decrypted_text += char
    return decrypted_text


if __name__ == "__main__":
    print(decrypt_vigenere("LXFOPVEFRNHR", "LEMON"))
