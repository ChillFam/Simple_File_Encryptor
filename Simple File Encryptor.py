import os
import time
import getpass
import tkinter as tk
from tkinter import filedialog
from Cryptodome.Cipher import AES
from Cryptodome.Protocol.KDF import PBKDF2

def decrypt_file(password, file_path, chunksize=64*1024):
    # Read the salt and initialization vector from the file
    with open(file_path, 'rb') as infile:
        salt = infile.read(16)
        iv = infile.read(16)
        ciphertext = infile.read()
    
    infile.close()
    
    # Derive key from password
    key = PBKDF2(password, salt, dkLen=32)
    decryptor = AES.new(key, AES.MODE_GCM, iv)
    filesize = os.path.getsize(file_path)

    # Decrypt the data
    original_data = decryptor.decrypt(ciphertext)

    # Remove padding from the data
    original_data = original_data.rstrip(b' ')

    # Write the decrypted data back to the same file
    with open(file_path, 'wb') as outfile:
        outfile.write(original_data)
            
    outfile.close()
    os.rename(file_path, file_path.replace(' ', '')[:-10])

def encrypt_file(password, file_path, chunksize=64*1024):
    # Derive key from password
    salt = os.urandom(16)
    key = PBKDF2(password, salt, dkLen=32)
    iv = os.urandom(16)
    encryptor = AES.new(key, AES.MODE_GCM, iv)
    filesize = os.path.getsize(file_path)

    with open(file_path, 'rb') as infile:
        # Read the original file
        original_data = infile.read()
        # Add padding to the data
        original_data += b' ' * (16 - len(original_data) % 16)
        # Encrypt the data
        ciphertext = encryptor.encrypt(original_data)

    # Write the encrypted data back to the same file
    with open(file_path, 'wb') as outfile:
        outfile.write(salt)
        outfile.write(iv)
        outfile.write(ciphertext)
        
    outfile.close()    
    os.rename(file_path, file_path + '.encrypted')
        

def main():
    print("Welcome to the Simple File Encryption/Decryption App")
    while True:
        print("\nPlease select an option:")
        print("1. Encrypt a file")
        print("2. Decrypt a file")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            root = tk.Tk()
            root.attributes('-topmost', True)
            root.withdraw()
            
            try:
                file_path = filedialog.askopenfilename()
                if file_path:
                    root.destroy()
                    #password = input("Enter the password: ")
                    password = getpass.getpass("Enter the password: ")
                    encrypt_file(password, file_path)
                    print("\nFile encrypted successfully")
                else:
                    print("\nNo file was selected")
            except Exception as e:
                print("\nAn error occurred: ", e)
        elif choice == '2':
            root = tk.Tk()
            root.attributes('-topmost', True)
            root.withdraw()
            
            try:
                file_path = filedialog.askopenfilename()
                if file_path:
                    root.destroy()
                    #password = input("Enter the password: ")
                    password = getpass.getpass("Enter the password: ")
                    decrypt_file(password, file_path)
                    print("\nFile decrypted successfully")
                else:
                    print("\nNo file was selected")
            except Exception as e:
                print("\nAn error occurred: ", e)
        elif choice == '3':
            exit(0)
        else:
            print("Invalid choice. Please enter a valid option (1-3)")

if __name__ == '__main__':
    main()