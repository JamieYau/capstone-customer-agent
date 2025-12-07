# app/__init__.py
import os
from pathlib import Path
from dotenv import load_dotenv

# Try to load .env if not already loaded from streamlit
if not os.getenv("OPENAI_API_KEY"):  # Check one critical var
    env_path = Path(__file__).parent.parent / '.env'
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
    else:
        print("Warning: .env file not found at", env_path)