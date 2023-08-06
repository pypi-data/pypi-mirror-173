import argparse

from datahub import utils

commands = {
    "configure": utils.cli_configure
}

def arg_parser():
    parser = argparse.ArgumentParser(description="""
    Datahub utils to manage the data repository configuration
    """)
    parser.add_argument("command", type=str, choices=commands.keys(), 
        help="utils command")

    return parser

def main(argv: str):
    parser = arg_parser()
    args = parser.parse_args(argv[1:2])
    
    commands[args.command](argv[2:])