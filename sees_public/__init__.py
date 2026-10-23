# SPDX-License-Identifier: MIT

from argparse import ArgumentParser
from importlib.metadata import version

from sees_public.sees_app import SEESApp

__version__ = version("sees_public")
__all__ = ["main"]


def main() -> None:
    parser = ArgumentParser(f"SEES Public {__version__}")
    subparsers = parser.add_subparsers(dest="mode", metavar="mode")

    # dev subcommand
    dev = subparsers.add_parser("dev", help="dev operations")
    dev.add_argument("-p", "--port", type=int, default=5001, help="port to run the development server on (default 5001)")

    args = parser.parse_args()

    if args.mode == "dev":
        SEESApp(dev_mode=True).run_dev(port=args.port)
    else:
        SEESApp(options={"config": "sees_public/config/gunicorn_config.py"}).run()
