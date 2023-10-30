"""install CLI command implementation."""
# dem/cli/install_cmd.py

from dem.cli.console import stdout, stderr
from dem.core.platform import DevEnvLocalSetup
from dem.core.dev_env import DevEnv

(
    DEV_ENV_LOCAL_NOT_AVAILABLE,
    DEV_ENV_LOCAL_REINSTALL,
    DEV_ENV_LOCAL_INSTALLED,
) = range(3)

dev_env_local_status_messages = {
    DEV_ENV_LOCAL_NOT_AVAILABLE: "[red]Error: Required image is not available![/]",
    DEV_ENV_LOCAL_REINSTALL: "Incomplete local install. The missing images are available in the registry. Use `dem pull` to reinstall.",
    DEV_ENV_LOCAL_INSTALLED: "Installed.",
}

# def get_dev_env(platform: DevEnvLocalSetup, dev_env_name: str) -> DevEnv:
#     """ Get the dev env named dev_env_name
#     Args:
#         TODO: Add args
#         """
#     dev_env = platform.get_dev_env_by_name(dev_env_name)
#     return dev_env

def get_dev_env_descriptor() -> dict:
    dev_env_descriptor = {
        "name": dev_env_name,
        "tools": []
    }

    for tool_type, tool_image in tool_selection.items():
        if "/" in tool_image:
            registry, image = tool_image.split("/")
            image_name = registry + '/' + image.split(":")[0]
        else:
            image = tool_image
            image_name = image.split(":")[0]
        tool_descriptor = {
            "type": tool_type,
            "image_name": image_name,
            "image_version": image.split(":")[1],
            "installed": True
            # "image_status": DEV_ENV_LOCAL_INSTALLED # Use this?
        }
        dev_env_descriptor["tools"].append(tool_descriptor)

    return dev_env_descriptor


def overwrite_existing_dev_env(original_dev_env: DevEnv, new_dev_env_descriptor: dict) -> None:
    original_dev_env.tools = new_dev_env_descriptor["tools"]


def install_dev_env(platform: DevEnvLocalSetup, dev_env: DevEnv) -> None:
    """ TODO Document
    Args:
        TODO: Add args
    """

    # Check image statuses before pulling
    image_statuses = dev_env.check_image_availability(platform.tool_images)

    tools_to_install = set()
    for tool in dev_env.tools:
        if tool.image_status == DEV_ENV_LOCAL_INSTALLED:
            # TODO: Saved for printing
            continue
        tools_to_install.append(tool)
        continue

    platform.pull_images(tools_to_install)

    # Get new descriptor
    new_dev_env_descriptor = get_dev_env_descriptor_from_user(dev_env_name, tool_image_list)
    # Overwrite old
    dev_env.tools = new_dev_env_descriptor["tools"]

    platform.flush_to_file()

    # In the Dev Env descriptor set the “installed” key to “True”."installed": "True",p

    return


def execute(dev_env_name: str) -> None:
    print('Test install')
    platform = DevEnvLocalSetup()
    print('Got platform')
    # dev_env = get_dev_env(platform, dev_env_name)
    dev_env = platform.get_dev_env_by_name(dev_env_name)
    print('Got dev env')

    if dev_env is None:
        stderr.print(\
                     """Usage: dem install [OPTIONS]
                     Try 'dem install --help' for help.

                     Error: No local dev environment named {} found""".format(dev_env_name))
        return

    install_dev_env(platform, dev_env)


if __name__ == '__main__':
    execute("Tutorial")

""" Development notes, REMOVE LATER

json path: "/.config/axem/dem"

command: dem install DEV_ENV_NAME

1. [X] The DEM looks for the DEV_ENV_NAME in the local dev_env.json.
   If the DEM can’t find the Dev Env, it should report an error for the user and stop the execution.
2. [X] The DEM pulls the images from the registries to the given host machines.
3. [ ] The DEM should inform the user about the successful operation if all the images are pulled.
       Maybe use:
        `
        table = Table()
        table.add_column("Development Environment")
        table.add_column("Status")
        table.add_row(dev_env.name, get_local_dev_env_status(dev_env, platform.tool_images))
        stdout.print(table)
        `
4. [ ] In the Dev Env descriptor set the “installed” key to “True”.
   "installed": "True",
5. [X] If the DEV_ENV_NAME is an empty parameter, the DEM shall raise an error. (Handled by typer.)
6. [ ] The DEM should autocomplete the DEV_ENV_NAME with the locally already available Dev Envs.
"""




