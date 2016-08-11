import six

from ..utils.is_base_type import is_base_type
from .options import Options

from .abstracttype import AbstractTypeMeta
from .utils import get_fields_in_type, yank_fields_from_attrs, merge_fields_in_attrs


class InterfaceMeta(AbstractTypeMeta):

    def __new__(cls, name, bases, attrs):
        # Also ensure initialization is only performed for subclasses of
        # Interface
        if not is_base_type(bases, InterfaceMeta):
            return type.__new__(cls, name, bases, attrs)

        options = Options(
            attrs.pop('Meta', None),
            name=name,
            description=attrs.get('__doc__'),
            interfaces=(),
        )

        attrs = merge_fields_in_attrs(bases, attrs)
        options.fields = get_fields_in_type(cls, attrs)
        yank_fields_from_attrs(attrs, options.fields)

        return type.__new__(cls, name, bases, dict(attrs, _meta=options))


class Interface(six.with_metaclass(InterfaceMeta)):
    resolve_type = None

    def __init__(self, *args, **kwargs):
        raise Exception("An interface cannot be intitialized")

    @classmethod
    def implements(cls, objecttype):
        pass