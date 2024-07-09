# 🦕 envtyped

This library is heavily inspired by [python-decouple](https://github.com/HBNetwork/python-decouple). Main goal is to provide a simple way to load environment variables, with type hinting, for my FastAPI projects.

## 📝 Table of Contents

- [📝 Table of Contents](#-table-of-contents)
- [📦 Installation](#-installation)
- [🚀 Usage](#-usage)
- [📝 License](#-license)

## 📦 Installation

```bash
pip install envtyped
```

## 🚀 Usage

```python
from envtyped import config

# Get environment variable, no need to do anything else, .env file is lazy loaded
SECRET_KEY = config.get("MY_ENV_VAR") # str

# You can cast the value to another type
DELAY_IN_SECONDS = config.get("DELAY_IN_SECONDS", cast=int) # int

# You can also use a custom function to cast the value
DELAY = config.get("DELAY", cast=lambda x: datetime.fromtimestamp(int(x))) # datetime

# If you need to, you also can use a custom class to cast the value, that can be constructed from a string
class Employee:
    def __init__(self, name: str) -> None:
        self.name = name.capitalize()

    def hello(self) -> str:
        return f"Hello {self.name}"


EMPLOYEE = config.get("EMPLOYEE", cast=Employee) # Employee
EMPLOYEE.hello()
# -> Hello John

# By default all env variables are required, but you can also set a default value
SECRET_KEY = config.get("SECRET_KEY", default="default_secret_key")

# Or you can set a value to be optional
SECRET_KEY = config.get("SECRET_KEY", optional=True) # Optional[str]


# This library provides a helpers to read csv 
from envtyped import Csv

AVAILABLE_LANGUAGES = config.get("AVAILABLE_LANGUAGES", cast=Csv()) # List[str]

# Csv can also be used to cast a list of string to a list of class
class Language:
    def __init__(self, name: str) -> None:
        self.name = name

AVAILABLE_LANGUAGES = config.get("AVAILABLE_LANGUAGES", cast=Csv(cast=Language)) # List[Language]

# Choise is a helper to limit the value to a list of choice
from envtyped import Choise

USER_LANGUAGE = config.get("USER_LANGUAGE", cast=Choise(["en", "fr"])) # str
USER_CURRENCY = config.get("USER_CURRENCY", cast=Choise(["usd", "eur"], default="usd")) # str


```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

With ❤️ 
