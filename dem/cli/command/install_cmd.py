"""install CLI command implementation."""
# dem/cli/install_cmd.py

from dem.cli.console import stdout, stderr
from dem.core.platform import DevEnvLocalSetup
from dem.core.dev_env import DevEnv

def get_dev_env(platform: DevEnvLocalSetup, dev_env_name: str) -> DevEnv:
    dev_env = platform.get_dev_env_by_name(dev_env_name)
    return dev_env


def pull_dev_env_image(platform: DevEnvLocalSetup, dev_env_name: str):
    if not platform.dev_env_catalogs.catalogs:
        stderr.print("[red]Error: No Development Environment Catalogs are available to pull the image from![/]")
        return

    

    return


def execute(dev_env_name: str) -> None:
    print('Test install')
    platform = DevEnvLocalSetup()
    dev_env = get_dev_env(platform, dev_env_name)
    if get_dev_env(platform, dev_env_name):
        return
    else:
        stderr.print(\
"""Usage: dem install [OPTIONS]
Try 'dem install --help' for help.

Error: No local dev environment named {} found""".format(dev_env_name))



""" Development notes, REMOVE LATER

command: dem install DEV_ENV_NAME

1. [X] The DEM looks for the DEV_ENV_NAME in the local dev_env.json.
   If the DEM can’t find the Dev Env, it should report an error for the user and stop the execution.
2. [ ] The DEM pulls the images from the registries to the given host machines.
3. [ ] The DEM should inform the user about the successful operation if all the images are pulled.
4. [ ] In the Dev Env descriptor set the “installed” key to “True”.
   "installed": "True",
5. [X] If the DEV_ENV_NAME is an empty parameter, the DEM shall raise an error. (Handled by typer.)
6. [ ] The DEM should autocomplete the DEV_ENV_NAME with the locally already available Dev Envs.
"""




