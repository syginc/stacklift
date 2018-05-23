#!/usr/bin/env python3

import click
from stacklift.read_config import ReadConfigOptions, read_config
from stacklift.validate_configs import validate_configs
from stacklift.deploy_group import deploy_group

@click.group()
def cli():
    pass

@cli.command(name="read_config")
@click.option("--file", "-f", required=True)
@click.option("--section", "-s", required=True)
@click.option("--default", "-d")
@click.option("--parameter", "-p", is_flag=True, default=False)
@click.argument("key", nargs=1)
def read_config_cli(file, section, default, parameter, key):
    opts = ReadConfigOptions()
    opts.file = file
    opts.section = section
    opts.default = default
    opts.parameter = parameter
    opts.key = key
    read_config(opts)

@cli.command(name="validate_configs")
@click.argument("files", nargs=-1)
def validate_config_cli(files):
    validate_configs(files=files)

@cli.command(name="deploy_group")
@click.option("--config-file", "-f", required=True)
@click.option("--group-file", "-g", required=True)
@click.option("--function-root", "-r")
def deploy_group_cli(config_file, group_file, function_root):
    deploy_group(config_file=config_file, group_file=group_file, function_root=function_root)


def run():
    cli()

if __name__ == '__main__':
    run()
