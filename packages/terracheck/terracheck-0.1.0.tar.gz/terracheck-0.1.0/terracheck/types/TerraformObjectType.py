from enum import Enum, EnumMeta

class MetaEnum(EnumMeta):
    def __contains__(cls, item):
        try:
            cls(item)
        except ValueError:
            return False
        return True    


class BaseEnum(Enum, metaclass=MetaEnum):
    pass

class TerraformObjectType(BaseEnum):
    OUTPUT            = "output"
    VARIABLE          = "variable"
    RESOURCE          = "resource"
    DATA              = "data"
    TERRAFORM         = "terraform"
    PROVIDER          = "provider"
    REQUIRED_PROVIDER = "required_providers"