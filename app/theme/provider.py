import json
import logging
from pathlib import Path
from typing import Dict, Any

logger = logging.getLogger(__name__)

class ThemeProvider:
    """Loads and provides design tokens from the JSON configuration."""
    
    _instance = None
    _tokens: Dict[str, Any] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ThemeProvider, cls).__new__(cls)
            cls._instance._load_tokens()
        return cls._instance

    def _load_tokens(self):
        token_path = Path("src/config/design_tokens.json")
        try:
            with open(token_path, "r", encoding="utf-8") as f:
                self._tokens = json.load(f)
            logger.info("Design tokens loaded successfully.")
        except FileNotFoundError:
            logger.warning(f"Design tokens not found at {token_path}. Using fallback.")
            self._tokens = {"color": {"brand": {"red": "#E50914"}}}
        except Exception as e:
            logger.error(f"Error loading design tokens: {e}")
            self._tokens = {}

    def get_tokens(self) -> Dict[str, Any]:
        """Returns the full parsed token dictionary."""
        return self._tokens
        
    def get_color(self, category: str, name: str) -> str:
        """Helper to get a specific color token."""
        return self._tokens.get("color", {}).get(category, {}).get(name, "#000000")

# Singleton instance
theme_provider = ThemeProvider()
