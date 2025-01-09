import rsa
import random
import string


class Encryptor:
    def __init__(self, public_key=None, encryption_type="rsa"):
        if public_key:
            self.public_key = public_key
        else:
            self.public_key, self.private_key = rsa.newkeys(512)  # Default RSA key size

        self.encryption_type = encryption_type

    def encrypt_text(self, text):
        """
        Encrypts text based on the chosen encryption type.
        Supported types: rsa, substitution, xor"
        """
        if self.encryption_type.lower() == "rsa":
            return rsa.encrypt(text.encode('utf-8'), self.public_key)
        
        elif self.encryption_type.lower() == "sub":
            return self.substitution_encrypt(text)
        
        elif self.encryption_type.lower() == "xor":
            return self.xor_encrypt(text, key=self.public_key)
    
        
        else:
            raise ValueError(f"Unsupported encryption type: '{self.encryption_type}'")


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
    
    def xor_encrypt(self, text, key):
        """
        Performs XOR encryption on the given text using the provided key.
        :param text: The plaintext to encrypt.
        :param key: The key used for XOR encryption.
        :return: Encrypted text as a string of characters.
        """
        # Repeat the key to match the length of the text
        extended_key = (key * ((len(text) // len(key)) + 1))[:len(text)]

        # XOR each character with the corresponding character from the extended key
        encrypted_chars = [chr(ord(c) ^ ord(k)) for c, k in zip(text, extended_key)]
        
        # Combine the encrypted characters into a single string
        encrypted_text = ''.join(encrypted_chars)
        return encrypted_text.encode('utf-8')

    def decrypt_substitution(self, encrypted_text, substitution_map):
        """
        Decrypts text encrypted with the substitution cipher.
        """
        reverse_map = {v: k for k, v in substitution_map.items()}
        decrypted_text = ''.join(reverse_map.get(char, char) for char in encrypted_text)
        return decrypted_text