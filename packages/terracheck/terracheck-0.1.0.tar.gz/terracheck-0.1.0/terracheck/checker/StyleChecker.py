from typing import Dict
from uuid import uuid4
from terracheck.types.TerraformObjectType import TerraformObjectType
from terracheck.types.TerraformBasicFileName import TerraformBasicFileName
from terracheck.types.RuleCategory import RuleCategory
from terracheck.types.CheckerElement import CheckerElement
from terracheck.types.CheckerIssue import CheckerIssue

class StyleChecker():

    def __init__(self) -> None:
        self.report = {}

    @staticmethod
    def _map_tf_object_type_to_file(terraform_object_type: TerraformObjectType) -> TerraformBasicFileName:
        if terraform_object_type.value == TerraformObjectType.OUTPUT.value:
            return TerraformBasicFileName.OUTPUTS_TF
        elif terraform_object_type.value == TerraformObjectType.VARIABLE.value:
            return TerraformBasicFileName.VARIABLES_TF
        elif terraform_object_type.value == TerraformObjectType.PROVIDER.value:
            return TerraformBasicFileName.VERSION_TF
        elif terraform_object_type.value == TerraformObjectType.REQUIRED_PROVIDER.value:
            return TerraformBasicFileName.VERSION_TF   
        else:
            return None 

    @staticmethod
    def _group_extract_by_unique_terraform_resource_type(hcl_reader_extract: Dict[str, CheckerElement]):
        resources_clusters = {}
        not_unique_resource_types = []
        for _, element in hcl_reader_extract.items():
            ert = element.terraform_resource_type
            if ert is not None:
                if ert in resources_clusters:
                    del resources_clusters[ert]
                    not_unique_resource_types.append(ert)
                elif ert in not_unique_resource_types:
                    pass
                else:
                    resources_clusters[ert] = element
                
        return resources_clusters

    def _check_no_dash_only_underscores_in_objects_names(self, hcl_reader_extract: Dict[str, CheckerElement]):
        for _, element in hcl_reader_extract.items():
            if element.terraform_object_type not in [TerraformObjectType.PROVIDER, TerraformObjectType.REQUIRED_PROVIDER]:
                dash_count = element.name.count('-')
                if dash_count >= 1:
                    resource_type_display = f"'{element.terraform_resource_type}'" if element.terraform_resource_type is not None else "named"
                    self.report[uuid4()] = CheckerIssue(
                        RuleCategory.NAME_HAS_DASH, 
                        f"Name of {element.terraform_object_type.value} {resource_type_display} '{element.name}' contains dash ('-'). Shoud be underscores ('_')."
                    )

    def _check_resource_name_is_not_resource_type(self, hcl_reader_extract: Dict[str, CheckerElement]):
        for _, element in hcl_reader_extract.items():
            if element.terraform_resource_type is not None and element.name == element.terraform_resource_type:
                self.report[uuid4()] = CheckerIssue(
                    RuleCategory.NAME_IS_RESOURCE, 
                    f"{element.terraform_object_type.value.capitalize()} '{element.terraform_resource_type}' is named '{element.name}'. Chose a name different than the resource name."
                )  

    def _check_output_variable_location(self, hcl_reader_extract: Dict[str, CheckerElement]):
        for _, element in hcl_reader_extract.items():
            expected_file = self._map_tf_object_type_to_file(element.terraform_object_type)
            if expected_file is not None and element.filename != expected_file.value:
                self.report[uuid4()] = CheckerIssue(
                    RuleCategory.FILE_PURPOSE,
                    f"{element.terraform_object_type.value.capitalize()} '{element.name}' should be declared in file {expected_file.value} not in {element.filename}."
                )

    def _check_output_exposure(self, hcl_reader_extract: Dict[str, CheckerElement]):
        for _, element in hcl_reader_extract.items():
            if element.terraform_object_type.value == TerraformObjectType.OUTPUT.value and "var." in element.additional_info["output_value"]:
                self.report[uuid4()] = CheckerIssue(
                    RuleCategory.OUTPUT_EXPOSURE,
                    f"Output '{element.name}' references a variable as value. It should not."
                )

    def _check_unique_resources_are_named_main(self, hcl_reader_extract: Dict[str, CheckerElement]):
        unique_resources = self._group_extract_by_unique_terraform_resource_type(hcl_reader_extract)
        for element in unique_resources.values():
            self.report[uuid4()] = CheckerIssue(
                    RuleCategory.NAME_UNIQUENESS,
                    f"{element.terraform_object_type.value.capitalize()} '{element.terraform_resource_type}' is unique, and thus should be named 'main', not '{element.name}'."
                )


    def check(self, hcl_reader_extract: Dict[str, CheckerElement]):
        
        self._check_no_dash_only_underscores_in_objects_names(hcl_reader_extract)
        self._check_resource_name_is_not_resource_type(hcl_reader_extract)
        self._check_output_variable_location(hcl_reader_extract)
        self._check_output_exposure(hcl_reader_extract)
        self._check_unique_resources_are_named_main(hcl_reader_extract)

        for id, issue in self.report.items():
            print(issue)
