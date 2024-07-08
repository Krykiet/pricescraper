import argparse


def get_config():
    parser = argparse.ArgumentParser(description="Run FastAPI with different DB url settings.")
    parser.add_argument("--local", action="store_true", help="Run the app in local mode.")
    parser.add_argument("--prod", action="store_true", help="Run the app in production mode.")
    parser.add_argument("--remote", action="store_true", help="Run the app in remote")

    return parser.parse_args()
