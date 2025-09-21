import json
import os
# We will import the function from your GUI file to launch it.
from first_time_config_gui import run_gui_setup

# --- Define a custom save area for the configuration ---
try:
    # This reliably gets the script's containing directory.
    SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
except NameError:
    # Fallback for environments where __file__ is not defined (e.g., interactive interpreter)
    SCRIPT_DIR = os.getcwd()
CONFIG_FILE = os.path.join(SCRIPT_DIR, "config.json")
# ---------------------------------------------------------

REQUIRED_KEYS = ["download_location", "default_quality"]

def _save_config(config_data: dict):
    """Saves the configuration dictionary to a JSON file."""
    os.makedirs(SCRIPT_DIR, exist_ok=True)
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config_data, f, indent=4)
    # print(f"✅ Configuration saved to {CONFIG_FILE}")

def _load_config() -> dict:
    """Loads the configuration from the JSON file."""
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)

def _run_config_setup():    
    # Call the GUI function to get user input.
    config_data = run_gui_setup()
    
    if config_data:
        _save_config(config_data)
        return config_data
    else:
        # print("❌ Setup was cancelled. Exiting application.")
        exit()

def _missing_config_setup():    
    # Call the GUI function to get user input.
    config_data = run_gui_setup()
    
    if config_data:
        _save_config(config_data)
        return config_data
    else:
        # print("❌ Setup was cancelled. Exiting application.")
        exit()        

def get_config() -> dict:
    """ 
    Loads configuration. Runs the GUI setup if the config file is
    missing or if any required settings are incomplete.
    """
    if not os.path.exists(CONFIG_FILE):
        # print(f"Configuration file not found in '{SCRIPT_DIR}'.")
        return _run_config_setup()
    
    try:
        config = _load_config()
        # print("config loaded") if config else print("config not loaded")
        missing_keys = [key for key in REQUIRED_KEYS if key not in config]
        
        if missing_keys:
            # print(f"⚠️ Your configuration is missing required settings: {missing_keys}.")
            return _missing_config_setup()
        
        print(f"📖 Configuration loaded successfully from {CONFIG_FILE}.")
        return config
    except (json.JSONDecodeError, IOError) as e:
        # print(f"❌ Error reading config file: {e}. Let's set it up again.")
        return _run_config_setup()

if __name__ == "__main__":
    # This allows you to test the config handler independently
    get_config()
