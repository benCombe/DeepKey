import os
import rsa
import random
import string
import sys
import lorem
from utils import ProgressBar, Spinner
from Encryptor import Encryptor

# Constants
NUM_FILES = 10000  # Number of file pairs to generate
OUTPUT_DIR = "Training"
DECRYPTED_DIR = os.path.join(OUTPUT_DIR, "decrypted")
ENCRYPTED_DIR = os.path.join(OUTPUT_DIR, "encrypted")



# Function to generate random text
def generate_random_text(length=50):
    return lorem.paragraph()[0:500]

# Function to ensure directories exist
def ensure_directories():
    DECRYPTED_DIR = os.path.join(OUTPUT_DIR, "decrypted")
    ENCRYPTED_DIR = os.path.join(OUTPUT_DIR, "encrypted")
    os.makedirs(DECRYPTED_DIR, exist_ok=True)
    os.makedirs(ENCRYPTED_DIR, exist_ok=True)

# Function to save text to a file
def save_to_file(filepath, content):
    with open(filepath, 'w') as file:
        file.write(content)

# Generate RSA keys
def generate_rsa_keys():
    public_key, private_key = rsa.newkeys(4096) # 4096-bit key (MAX 501 char)
    return public_key, private_key

# Encrypt text using RSA
def encrypt_text(text, public_key):
    return rsa.encrypt(text.encode('utf-8'), public_key)


def generate_files():
    # Generate RSA keys
    spinner = Spinner("Generating Keys (this will take a minute)")
    spinner.start()
    try:
        public_key, private_key = generate_rsa_keys()
        encr = Encryptor(public_key)
    finally:
        spinner.stop()
    pb = ProgressBar(NUM_FILES, 50, f"Generating {OUTPUT_DIR} Data")

    for i in range(1, NUM_FILES + 1):
        pb.update(i)
        # Generate random text
        random_text = generate_random_text()

        # File identifiers
        if OUTPUT_DIR == "Training":
            file_id = f"tr_{i:05d}"
        elif OUTPUT_DIR =="Testing":
            file_id = f"te_{i:05d}"

        # File paths
        decrypted_path = os.path.join(DECRYPTED_DIR, f"{file_id}.dec")
        encrypted_path = os.path.join(ENCRYPTED_DIR, f"{file_id}.enc")

        # Encrypt the random text
        encrypted_text = encr.encrypt_text(random_text, "rsa")

        # Save the files
        save_to_file(decrypted_path, random_text)
        with open(encrypted_path, 'wb') as enc_file:
            enc_file.write(encrypted_text)

    print(f"\n\nFile generation complete. {NUM_FILES*2} Files Created.")


# Main script
if __name__ == "__main__":
    
    if len(sys.argv) > 1:
        if sys.argv[1].lower() == "training":
            OUTPUT_DIR = "Training"
        elif sys.argv[1].lower == "testing":
            OUTPUT_DIR = "Testing"
        else:
            while True:
                response = input("Data Type Not recognised. Did you want to create Training or Testing data? ")
                if response.lower() == "training":
                    OUTPUT_DIR = "Training"
                    break
                elif response.lower() == "testing":
                    OUTPUT_DIR = "Testing"
                    break                 
    else:
        response = input("Did you want to create Training or Testing data? ")
        while True:
            if response == "training":
                    OUTPUT_DIR = "Training"
                    break
            elif response == "testing":
                OUTPUT_DIR = "Testing"
                break  
            else:
                response = input("Data Type Not recognised. Did you want to create Training or Testing data? ")

    while True:
        num_data = input("Number of Entries: ")
        if int(num_data) and int(num_data) <= 10000:
            NUM_FILES = int(num_data)
            break
        elif int(num_data) > 10000:
            print("Number Too Large (MAX: 10000)")
        else:
            print("Please Enter a Number")
        

    # Ensure directory structure exists
    ensure_directories()

    generate_files()
