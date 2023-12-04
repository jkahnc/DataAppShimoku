from os import getenv
from dotenv import load_dotenv

import shimoku_api_python as Shimoku

from salesBoard import Dashboard

def main():
    # Load .env file
    load_dotenv()

    # Import enrivomental variable
    access_token = getenv('SHIMOKU_TOKEN')
    universe_id: str = getenv('UNIVERSE_ID')
    workspace_id: str = getenv('WORKSPACE_ID')

    # Client connection
    client_connect = Shimoku.Client(
        access_token=access_token,
        universe_id=universe_id,
    )

    client_connect.set_workspace(uuid=workspace_id)

    # Set Dashboard object
    board = Dashboard(client_connect)
    board.setDashboard()

if __name__ == "__main__":
  main()
