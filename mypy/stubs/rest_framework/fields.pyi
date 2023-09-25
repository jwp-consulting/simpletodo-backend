from typing import (
    Any,
)

class empty: ...

class Field:
    def __init__(
        self,
        read_only: bool = False,
        write_only: bool = False,
        allow_null: bool = False,
    ) -> None: ...

class BooleanField(Field): ...
class CharField(Field): ...
class EmailField(Field): ...
class RegexField(Field): ...
class SlugField(Field): ...
class URLField(Field): ...
class UUIDField(Field): ...
class IPAddressField(Field): ...
class IntegerField(Field): ...
class FloatField(Field): ...
class DateTimeField(Field): ...
class DateField(Field): ...
class TimeField(Field): ...
class DurationField(Field): ...
class ChoiceField(Field): ...
class MultipleChoiceField(Field): ...
class FilePathField(Field): ...
class FileField(Field): ...
class ImageField(Field): ...

class ListField(Field):
    def __init__(self, child: Field, **args: Any) -> None: ...

class DictField(Field): ...
class HStoreField(Field): ...
class JSONField(Field): ...
class ReadOnlyField(Field): ...
class HiddenField(Field): ...
class SerializerMethodField(Field): ...
class ModelField(Field): ...
