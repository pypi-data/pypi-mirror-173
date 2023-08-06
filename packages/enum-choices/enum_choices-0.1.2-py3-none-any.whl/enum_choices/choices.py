import enum
from collections import OrderedDict

__all__ = ['Choices', 'BoolIntTypeChoice']


class ChoicesMeta(enum.EnumMeta):
    def __new__(metacls, classname, bases, classdict, **kwds):
        choices = []
        choices_map = OrderedDict()
        # enum.EnumMeta
        for key in classdict._member_names:
            value = classdict[key]
            if isinstance(value, (list, tuple)) and len(value) != 2:
                raise ValueError(f"key:{key} value:{value} v length !=2 ")
            num, label = value
            choices.append(value)
            choices_map[num] = label
            dict.__setitem__(classdict, key, num)
        cls = super().__new__(metacls, classname, bases, classdict, **kwds)
        # 注入_choices_map
        cls._choices_map = choices_map
        cls._choices = choices
        cls.do_not_call_in_templates = True
        return enum.unique(cls)

    def __contains__(cls, member):
        if not isinstance(member, enum.Enum):
            # Allow non-enums to match against member values.
            return any(x.value == member for x in cls)
        return super().__contains__(member)

    @property
    def names(cls):
        empty = ['__empty__'] if hasattr(cls, '__empty__') else []
        return empty + [member.name for member in cls]

    @property
    def choices(cls):
        return cls._choices

    @property
    def choices_map(cls):
        return cls._choices_map

    @property
    def labels(cls):
        return [label for _, label in cls.choices]

    @property
    def values(cls):
        return [value for value, _ in cls.choices]
    
    @property
    def iter(cls):
        """
        ",".join(c.iter): v1:v1_str,v2:v2_str,...
        """
        for value, value_str in cls.choices:
            yield "{}:{}".format(value, value_str)



class Choices(enum.IntEnum, metaclass=ChoicesMeta):
    def __str__(self):
        return str(self.value)


class BoolIntTypeChoice(Choices):
    """
    BoolIntTypeChoice: YES/NO
    """
    NO = (0, 'no')
    YES = (1, 'yes')
