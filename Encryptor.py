import rsa
import random
import string


class Encryptor:
    def __init__(self, public_key=None):
        if public_key:
            self.public_key = public_key
        else:
            self.public_key, self.private_key = rsa.newkeys(512)  # Default RSA key size

    def encrypt_text(self, text, encryption_type="rsa"):
        """
        Encrypts text based on the chosen encryption type.
        Supported types: "rsa", "substitution"
        """
        if encryption_type.lower() == "rsa":
            return rsa.encrypt(text.encode('utf-8'), self.public_key)
        
        elif encryption_type.lower() == "substitution":
            return self.substitution_encrypt(text)
        
        else:
            raise ValueError(f"Unsupported encryption type: {encryption_type}")


    # Change?
    def substitution_encrypt(self, text):
        """
        Performs 1:1 character substitution encryption.
        The substitution cipher will map each character to a pseudo-random other character.
        """
        # Generate a random substitution mapping
        characters = string.ascii_letters + string.digits + string.punctuation + " "
        shuffled = list(characters)
        random.shuffle(shuffled)
        substitution_map = dict(zip(characters, shuffled))

        # Encrypt the text
        encrypted_text = ''.join(substitution_map.get(char, char) for char in text)
        return encrypted_text

    def decrypt_substitution(self, encrypted_text, substitution_map):
        """
        Decrypts text encrypted with the substitution cipher.
        """
        reverse_map = {v: k for k, v in substitution_map.items()}
        decrypted_text = ''.join(reverse_map.get(char, char) for char in encrypted_text)
        return decrypted_text