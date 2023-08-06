from terracheck.types import TerraformObjectType

class CheckerElement():

    def __init__(self, name: str, path: str, terraform_object_type: TerraformObjectType, terraform_resource_type: str, additional_info={}) -> None:
        self.name                    = name
        self.path                    = path
        self.filename                = self.path.split('/')[-1]
        self.terraform_object_type   = terraform_object_type
        self.additional_info         = additional_info
        self.terraform_resource_type = terraform_resource_type

    def to_dict(self):
        return {
            'name': self.name,
            'path': self.path,
            'filename': self.filename,
            'terraform_object_type': self.terraform_object_type.value,
            'additional_info': self.additional_info,
            'terraform_resource_type': self.terraform_resource_type,
        }