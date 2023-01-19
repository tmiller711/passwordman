import click

@click.group()
@click.version_option(package_name='passwordman')
def main():
    """
    Commands to manage your passwords
    """
    pass