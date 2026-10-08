import os
import sys

# Entrypoint launcher script for EcoPlate AI
if __name__ == '__main__':
    from server import run_server
    port = int(os.environ.get("PORT", 8000))
    run_server(port)
