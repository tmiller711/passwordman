import click
import os
import pathlib
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
import hashlib

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

def get_path():
    return pathlib.Path(__file__).parent.resolve()

def get_file_dir():
    try:
        with open(f"{get_path()}/location.txt", "r") as file:
            return file.read().strip()
    
    except:
        click.echo(click.style("Need to specify the directory of encrypted file", fg='red'))

def unlock_account():
    password_attempt = click.prompt("What is your master password?")

    with open(f"{get_path()}/password.txt", "r") as file:
        password_hash = file.read()

        hashed_attempt = hashlib.sha256(password_attempt.encode())
        if password_hash == hashed_attempt.hexdigest():
            click.echo(click.style("Successfully Logged In!", fg="green"))
        else:
            click.echo(click.style("Incorrect Password", fg="red"))
            exit()

def decrypt_data(file, password):
    salt = b''
    password = 'password'

    key = PBKDF2(password, salt, dkLen=32)

    # with open('encrypted.bin', 'rb') as f:
    #     iv = f.read(16)
    #     decrypt_data = f.read()
    iv = file.read(16)
    to_decrypt = file.read()

    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    return unpad(cipher.decrypt(to_decrypt), AES.block_size)

def encrypt_data(data_to_encrypt, password):
    salt = b''

    key = PBKDF2(password, salt, dkLen=32)

    cipher = AES.new(key, AES.MODE_CBC)
    ciphered_data = cipher.encrypt(pad(data_to_encrypt, AES.block_size))
    return ciphered_data

    # with open('encrypted.bin', 'wb') as f:
    #     f.write(cipher.iv)
    #     f.write(ciphered_data)

@click.group()
@click.version_option(package_name='passwordman')
def main():
    """
    Commands to manage your passwords
    """
    pass

@click.command(name='setup')
def setup():
    """
    Set the directory of encrypted file
    """
    # if file and password already exist, ask them for the previous pass
    # create a master password
    master_pass = click.prompt("What would you like the master password to be?")
    with open(f"{get_path()}/password.txt", "w") as file:
        hashed_pass = hashlib.sha256(master_pass.encode())
        file.write(hashed_pass.hexdigest())

    directory = click.prompt("What is the full directory you would like to store your file?")

    with open(f"{directory}/passwordman.bin", 'wb') as f:
        pass

    with open(f"{get_path()}/location.txt", "w") as file:
        file.write(directory + "/passwordman.bin")

    click.echo(click.style("Successfully created file", fg='green'))

@click.command(name='create')
def create_password():
    """
    Create a new password entry
    """
    unlock_account()

    # get the new entry and then append it to the encrypted file
    company = click.prompt("What is the name of the company?")
    password = click.prompt("What is the password you want to save?")

    # first need to decrypt data and then add it to the decrypted data and then encrypt it?
    with open(get_file_dir(), 'rb') as file:
        decrypt_file(file, )

main.add_command(setup)
main.add_command(create_password)