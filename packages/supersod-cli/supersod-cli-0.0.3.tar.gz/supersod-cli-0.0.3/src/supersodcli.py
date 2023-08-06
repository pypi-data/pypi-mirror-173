""" Entrypoint of the CLI """
import click

from src.commands import authorize, polling


@click.group()
def cli():
    pass


@cli.command()
@click.option('-d', '--days', default=10, type=int)
def poll(days: int):
    """
    Query the singleops database over the last d days, default is 10

    $ supersod poll

    $ supersod poll -d 40
    """
    polling.poll(days)


@cli.command()
@click.option("--check", is_flag=True, default=False, help="Check the current API key.")
@click.option("-k", "--key", default=None, help="Update the Azure API key.", type=str)
@click.option("-n", "--name", default="AZURE_ONFLEET_API_KEY", help="Name of the value in the keychain.", type=str)
def auth(check: bool, key: str, name: str):
    """
    Check your Azure Onfleet Function App API Key or add a new API key

    $ supersod auth -k <API_KEY>

    $ supersod auth --check
    """
    authorize.auth(check, key, name)
