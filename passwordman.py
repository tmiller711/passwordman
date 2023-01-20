import click
import os
import pathlib

def get_path():
    return pathlib.Path(__file__).parent.resolve()

def get_file_dir():
    try:
        with open(f"{get_path()}/location.txt", "r") as file:
            return file.read().strip()
    
    except:
        click.echo(click.style("Need to specify the directory of encrypted file", fg='red'))

@click.group()
@click.version_option(package_name='passwordman')
def main():
    """
    Commands to manage your passwords
    """
    pass

@click.command(name='setdir')
def setdir():
    """
    Set the directory of encrypted file
    """
    directory = click.prompt("What is the full directory you would like to store your file?")

    with open(f"{directory}/passwordman.bin", 'wb') as f:
        pass

    with open(f"{get_path()}/location.txt", "w") as file:
        file.write(directory)

    click.echo(click.style("Successfully created file", fg='green'))

main.add_command(setdir)