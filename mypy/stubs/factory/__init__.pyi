from typing import (
    Any,
    Callable,
    Generic,
    Sequence,
    Type,
    TypeVar,
    Union,
)

T = TypeVar("T")

class Faker:
    def __init__(self, kind: str, *args: Any, **kwargs: Any) -> None: ...

class Factory(Generic[T]):
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    @classmethod
    def create(cls, *args: Any, **kwargs: Any) -> T: ...
    @classmethod
    def create_batch(
        cls, size: int, *args: Any, **kwargs: Any
    ) -> Sequence[T]: ...

class SubFactory:
    def __init__(
        self, sub_factory: Union[str, Type[Factory[Any]]]
    ) -> None: ...

class LazyAttribute:
    def __init__(self, fn: Callable[[Any], Any]) -> None: ...

# Change Any to Factory, somehow...
PostGenerationHook = Callable[[Any, bool, Any], None]

def post_generation(hook: PostGenerationHook) -> PostGenerationHook: ...
