from typing import (
    Any,
    Optional,
)

class ConfigurationBase(type): ...

class Configuration(metaclass=ConfigurationBase):
    DOTENV_LOADED: Optional[str]
    @classmethod
    def load_dotenv(cls) -> None: ...
    @classmethod
    def pre_setup(cls) -> None: ...
    @classmethod
    def post_setup(cls) -> None: ...
    @classmethod
    def setup(cls) -> None: ...
