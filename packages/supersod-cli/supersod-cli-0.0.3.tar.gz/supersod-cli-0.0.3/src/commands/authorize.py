import keyring
import keyring.util.platform_ as keyring_platform
from click import secho, confirm

import sys


# print(keyring_platform.config_root())
# /home/username/.config/python_keyring  # Might be different for you

# print(keyring.get_keyring())
# keyring.backends.SecretService.Keyring (priority: 5)


def auth(check: bool, key: str, name: str):
    if not any((check, key)):
        secho('No arguments supplied. See --help for arguments.', err=True)

    current_key = keyring.get_password('onfleet', name)

    if key and current_key:
        secho(f"API Key already set and will be overwritten", bold=True)
        if confirm("Continue?"):
            keyring.set_password('onfleet', name, key)
            sys.exit(0)
    elif key:
        keyring.set_password('onfleet', name, key)
        secho('Key set.')
    current_key = keyring.get_password('onfleet', name)

    if check and current_key:
        secho(f"{name}: {current_key}")
    elif check:
        secho(f"No Onfleet key found. Set with supersod auth -k <API_KEY_HERE>", bg='yellow')


# auth(False, '')
