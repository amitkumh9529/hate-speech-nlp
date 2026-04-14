import sys
import os
from streamlit.web import cli as stcli

if __name__ == "__main__":
    # Launch the Streamlit UI
    ui_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ui.py")
    sys.argv = ["streamlit", "run", ui_path, "--server.port=8080"]
    stcli.main()
