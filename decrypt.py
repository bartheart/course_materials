from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import os

# function to decrypt a fi;e 
def decrypt_file(file_path:str, key:str) -> None:
    # open the file to be decrypted     
    try:
        # open the file 
        with open(file_path, 'rb') as encrypted_file:
            # fetch the IV value 
            iv = encrypted_file.read(16)

            # read the the encrypted content 
            cipher_text = encrypted_file.read()

        # initaiate the AES cipher with the parameters
        cipher = AES.new(key, AES.MODE_CFB, iv)

        # decrypt the content
        plain_text = cipher.decrypt(cipher_text)


        # wirte the decrypted content into a new file 
        with open(file_path.replace(".enc", ""), "wb") as decrypted_file:
            decrypted_file.write(plain_text)
        
        # remove the encrypted file 
        os.remove(file_path)

            
    except Exception as e:
        print(f"Error decrypting {file_path}: {e}")



# function to decrypt files in directory
def decrypt_directory(directory:str, key:str) -> None:
    # explore the given directory 
    for root, dirs, files in os.walk(directory):
        # iterate over the files 
        for file in files:
            # check for an encrypted file 
            if file.endswith(".enc"):
                # decrypt the file 
                decrypt_file(os.path.join(root, file), key)


# function to give instructions how to decrypt the file 
def print_instructions():
    print("\nTo decrypt your files, please follow the instructions below:")


if __name__ == "__main__":
    print_instructions()

    # input the encryption key 
    key_input = input("Enter the decryption key: ")
 
    try:
        # Convert the key from string to bytes
        key = bytes.fromhex(key_input)
    except ValueError:
        print("Invalid key format. Please ensure the key is in hexadecimal format.")
        exit(1)

    # Decrypt the directory
    print("\nDecrypting files...")
    decrypt_directory("test", key)

    # Display completion message
    print("\nDecryption complete. All encrypted files have been restored.")

