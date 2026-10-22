# SPDX-License-Identifier: MIT

import argparse
import subprocess
import urllib3

from sees_public import create_flask_app

app = create_flask_app()


def main() -> None:
    """Main entry point for the application."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="SEES Public App")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug")
    parser.add_argument("-p", "--port", type=int, help="Port to run the server on. Default port is 5000.")
    args = parser.parse_args()

    # Run the Flask app
    if args.debug:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        app.run(host="0.0.0.0", port=args.port if args.port else 5000, debug=True)
    else:
        subprocess.run(["gunicorn", "-c", "sees_public/config/gunicorn_config.py", "FlaskServer:app"], check=False)


if __name__ == "__main__":
    main()
