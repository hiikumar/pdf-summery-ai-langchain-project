"""Configuration helper.

Reads a setting from Streamlit secrets when the app is deployed (Streamlit
Community Cloud exposes the Secrets manager through `st.secrets`), and falls
back to the process environment otherwise (locally, values come from `.env`).
"""

import os

from dotenv import load_dotenv

load_dotenv()


def get_secret(name: str, default=None):
    """Return `name` from Streamlit secrets if present, else from the environment."""
    try:
        import streamlit as st

        if name in st.secrets:
            return st.secrets[name]
    except Exception:  # noqa: BLE001 - st.secrets raises when no secrets file is configured
        pass
    return os.getenv(name, default)
