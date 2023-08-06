from enum import Enum

class TerraformBasicFileName(Enum):
    VARIABLES_TF = "variables.tf"
    OUTPUTS_TF   = "outputs.tf"
    VERSION_TF   = "versions.tf"
    README_MD    = "README.MD"
    README_md    = "README.md"