import os
import argparse

from pathlib import Path

def cli_configure(argv: str = ""):
    args = configure_parser(argv)
    credentials = {}
    credentials["aws_access_key_id"] = args.access_key_id if not args.access_key_id is None else input("Enter Access Key ID:")
    credentials["aws_secret_access_key"] = args.secret_access_key if not args.secret_access_key is None else input("Enter Secret Access key:")

    config = {}
    config["region"] = args.region if not args.region is None else input("Enter Region:")

    configure(credentials, config)

def configure(credentials: dict, config: dict):
    """
    """
    cfg_path = get_cfg_path()
    os.makedirs(cfg_path, exist_ok=True)

    write_cfg_file(cfg_path / "credentials", credentials)
    write_cfg_file(cfg_path / "config", config)

def get_cfg_path():
    return Path.home() / ".aws"

def write_cfg_file(cfg_path: str, content: dict):
    cfgd = open(cfg_path, "w")
    cfgd.write("[default]\n")
    
    for key, val in content.items():
        cfgd.write(f"   {key}={val}\n")
    
    cfgd.close()


def configure_parser(argv: str = ""):
    parser = argparse.ArgumentParser(description="Configuration commad")
    parser.add_argument("--access-key-id", type=str, default=None, help="aws access key")
    parser.add_argument("--secret-access-key", type=str, default=None, help="aws secret key")
    parser.add_argument("--region", type=str, default=None, help="region. may be depault, central1 or other, see aws documentation")
    
    return parser.parse_args(argv)