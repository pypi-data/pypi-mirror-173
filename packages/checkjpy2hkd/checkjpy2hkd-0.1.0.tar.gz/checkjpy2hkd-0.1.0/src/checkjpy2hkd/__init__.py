# __init__.py

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

from importlib import resources

# Version of the package
__version__ = "0.1.0"

# Read configuration file
CONFIG = tomllib.loads(resources.read_text("checkjpy2hkd", "config.toml", encoding="utf-8"))