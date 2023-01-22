import click
import os
import pathlib
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
import hashlib
import base64

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
            return password_attempt
        else:
            click.echo(click.style("Incorrect Password", fg="red"))
            exit()

def decrypt_data_from_file(file, password):
    salt = b''
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256,
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    f = Fernet(key)
    
    data_to_decrypt = file.read()
    return f.decrypt(data_to_decrypt)

def encrypt_data_to_file(file, data_to_encrypt, password):
    salt = b''

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256,
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))

    f = Fernet(key) 
    encrypted_data = f.encrypt(data_to_encrypt.encode())
    
    file.write(encrypted_data)

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
def create_entry():
    """
    Create a new password entry
    """
    master_pass = unlock_account()

    # get the new entry and then append it to the encrypted file
    company = click.prompt("What is the name of the company?")
    password = click.prompt("What is the password you want to save?")
    entry = f"{company} : {password}"

    # first need to decrypt data and then add it to the decrypted data and then encrypt it?
    if os.path.getsize(get_file_dir()) == 0:
        # if you haven't made any entries
        with open(get_file_dir(), 'wb') as file:
            encrypt_data_to_file(file, entry, master_pass)

    else:
        with open(get_file_dir(), 'rb') as file:
            decrypted_data = decrypt_data_from_file(file, master_pass)
        
        with open(get_file_dir(), 'wb') as file:
            data = (decrypted_data.decode() + '\n' + entry)
            encrypt_data_to_file(file, data, master_pass)

@click.command(name='entries')
def entries():
    """
    View all your password entries
    """
    master_pass = unlock_account()

    with open(get_file_dir(), 'rb') as file:
        decrypted_data = decrypt_data_from_file(file, master_pass)
        print(decrypted_data.decode())

main.add_command(setup)
main.add_command(create_entry)
main.add_command(entries)