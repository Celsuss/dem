"""install CLI command implementation."""
# dem/cli/install_cmd.py

from dem.core.platform import DevEnvLocalSetup
from dem.core.tool_images import ToolImages
from dem.cli.console import stdout, stderr
from dem.core.dev_env import DevEnv
from rich.table import Table

(
    DEV_ENV_LOCAL_NOT_AVAILABLE,
    DEV_ENV_LOCAL_REINSTALL,
    DEV_ENV_LOCAL_INSTALLED,
) = range(3)

image_status_messages = {
    ToolImages.NOT_AVAILABLE: "[red]Error: Required image is not available![/]",
    ToolImages.LOCAL_ONLY: "Image is available locally.",
    ToolImages.REGISTRY_ONLY: "Image is available in the registry.",
    ToolImages.LOCAL_AND_REGISTRY: "Image is available locally and in the registry.",
}

dev_env_local_status_messages = {
    DEV_ENV_LOCAL_NOT_AVAILABLE: "[red]Error: Required image is not available![/]",
    DEV_ENV_LOCAL_REINSTALL: "Incomplete local install. The missing images are available in the registry. Use `dem pull` to reinstall.",
    DEV_ENV_LOCAL_INSTALLED: "Installed.",
}

def get_dev_env_names() -> []:
    platform = DevEnvLocalSetup()
    local_dev_envs = []
    for local_dev_env in platform.local_dev_envs:
        local_dev_envs.append(local_dev_env.name)
    return local_dev_envs

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


def print_results(newly_installed_tools: [], installed_tools: [], tools_not_available) -> None:
    tool_info_table = Table()
    tool_info_table.add_column("Image")
    tool_info_table.add_column("Status")

    for tool in newly_installed_tools:
        tool_info_table.add_row(tool["image_name"] + tool["image_version"],
                                dev_env_local_status_messages[tool["image_status"]])
    for image in installed_tools:
        tool_info_table.add_row(tool["image_name"] + tool["image_version"],
                                dev_env_local_status_messages[tool["image_status"]])
    for image in tools_not_available:
        tool_info_table.add_row(tool["image_name"] + tool["image_version"],
                                dev_env_local_status_messages[tool["image_status"]])

    stdout.print(tool_info_table)


def install_dev_env(platform: DevEnvLocalSetup, dev_env: DevEnv) -> None:
    """ TODO Document
    Args:
        TODO: Add args
    """

    # Check image statuses before pulling
    image_statuses = dev_env.check_image_availability(platform.tool_images)

    tools_to_install = []
    installed_tools = []
    tools_not_available = []

    for tool, image_status in zip(dev_env.tools, image_statuses):
        if image_status == DEV_ENV_LOCAL_INSTALLED:
            installed_tools.append(tool)
        elif image_status == DEV_ENV_LOCAL_NOT_AVAILABLE:
            tools_not_available.append(tool)
        else:
            tools_to_install.append(tool)

    if len(tools_to_install) == 0:
        print_results(tools_to_install, installed_tools, tools_not_available)
        return

    print_results(tools_to_install, installed_tools, tools_not_available)

    # platform.pull_images(tools_to_install)

    # Get new descriptor
    # new_dev_env_descriptor = get_dev_env_descriptor(dev_env_name, )
    # Overwrite old
    # dev_env.tools = new_dev_env_descriptor["tools"]
    # platform.flush_to_file()

    return


def execute(dev_env_name: str) -> None:
    platform = DevEnvLocalSetup()
    dev_env = platform.get_dev_env_by_name(dev_env_name)

    if dev_env is None:
        stderr.print(\
                     """Usage: dem install [OPTIONS]
                     Try 'dem install --help' for help.

                     Error: No local dev environment named {} found""".format(dev_env_name))
        return

    install_dev_env(platform, dev_env)


if __name__ == '__main__':
    # get_dev_env_names()
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




