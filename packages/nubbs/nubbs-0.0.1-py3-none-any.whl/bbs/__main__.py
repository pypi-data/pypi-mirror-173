import glob

import click
import uvicorn

from starlette.applications import Starlette
from starlette.routing import Mount

import toml

from .core import BBS

from . import DEBUG
from . import DEFAULT_HOST
from . import DEFAULT_PORT
from . import L

from .config import BBSConfigBase


@click.group
def cli():
    pass


def app_factory(path, debug=DEBUG):

    routes: list[Mount] = list()

    bbs_loaders = glob.glob(f"{path}/*.bbs")

    for conf_file in bbs_loaders:

        L("Running", f"'{conf_file}'")

        config_dict = toml.load(conf_file)
        config = BBSConfigBase(**config_dict)

        bbs_application = BBS(bbs_config=config)

        # mount = Mount(f"/{config_dict['uri']}", bbs_application.api)
        mount = Mount(f"/{config.uri}", bbs_application.api)

        routes.append(mount)

    return Starlette(debug=debug, routes=routes)


if DEBUG:
    APP = app_factory(path=".")


@cli.command
@click.option("-l", "--host", "host", default=DEFAULT_HOST, type=str,
              help="IPv4 to listen. '0.0.0.0' to listen to all.")
@click.option("-p", "--port", "port", default=DEFAULT_PORT, type=int,
              help="Port to listen.")
@click.argument("path")
def run(path, host=DEFAULT_HOST, port=DEFAULT_PORT):

    if DEBUG:
        uvicorn.run("bbs.__main__:APP", host=host, port=port, reload=True)
        exit(0)

    # else:
    app = app_factory(path)
    uvicorn.run(app, host=host, port=port)


@cli.command
@click.argument("sites", nargs=-1)
def init(sites):

    for uri in sites:
        new_config = BBSConfigBase(uri=uri).dict()
        L(new_config)
        new_config_toml = toml.dumps(new_config)

        file_name = f"{uri}.bbs"
        with open(file_name, "a") as config_file:
            config_file.write(new_config_toml)
            L("Created file", file_name)


if __name__ == "__main__":
    cli()
