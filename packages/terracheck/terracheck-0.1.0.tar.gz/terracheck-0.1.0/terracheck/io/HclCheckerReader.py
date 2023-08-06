import logging
import json
from uuid import uuid4

from terracheck.types.CheckerElement import CheckerElement
from terracheck.types.TerraformObjectType import TerraformObjectType

class HclCheckerReader():

    def __init__(self) -> None:
        self.extract      = {}
        self.checker_elements_ids = {
            TerraformObjectType.RESOURCE : [],
            TerraformObjectType.DATA : [],
            TerraformObjectType.VARIABLE : [],
            TerraformObjectType.OUTPUT : [],
            TerraformObjectType.TERRAFORM: [],
            TerraformObjectType.PROVIDER: []
        }

    @staticmethod
    def _get_tf_files_paths(folder: str):
        import os
        from os.path import isfile, join
        import glob

        # List .tf files in the folder
        tf_globs = glob.glob(join(folder,"*.tf"))
        # Keep files only
        tf_files = [f for f in tf_globs if isfile(f)]
        return tf_files

    @staticmethod
    def _get_hcl_content(file_path):
        import hcl2

        with open(file_path) as pfile:
            hcl_file = hcl2.load(pfile)
            return hcl_file

    def _read_resource_data(self, hcl_content: dict, terraform_object_type: TerraformObjectType, file_path: str):
        for terraform_resource in hcl_content:
            # print(json.dumps(hcl_content, indent=4))
            terraform_resource_type = list(terraform_resource.keys())[0]
            terraform_resource_given_name = list(terraform_resource[terraform_resource_type].keys())[0]
            checker_element = CheckerElement(
                                terraform_resource_given_name, 
                                file_path, 
                                terraform_object_type,
                                terraform_resource_type
                                )
            unique_id = uuid4()
            self.extract[unique_id] = checker_element
            self.checker_elements_ids[terraform_object_type].append(unique_id)

    def _read_variable_output(self, hcl_content: dict, terraform_object_type: TerraformObjectType, file_path: str):
        for terraform_resource in hcl_content:
            terraform_resource_type = list(terraform_resource.keys())[0]
            # next_key = list(terraform_resource[terraform_resource_type].keys())[0]
            additional_info = {}
            if terraform_object_type == TerraformObjectType.OUTPUT:
                additional_info["output_value"] = terraform_resource[terraform_resource_type]["value"]
            checker_element = CheckerElement(
                                terraform_resource_type, 
                                file_path, 
                                terraform_object_type,
                                None,
                                additional_info
                                )
            unique_id = uuid4()
            self.extract[unique_id] = checker_element
            self.checker_elements_ids[terraform_object_type].append(unique_id)

    def _read_terraform(self, hcl_content: dict, terraform_object_type: TerraformObjectType, file_path: str):
        for provider_alias_setup in hcl_content:
            required_providers = provider_alias_setup.get(TerraformObjectType.REQUIRED_PROVIDER.value, {})
            for alias_dict in required_providers:
                for alias in alias_dict:
                    checker_element = CheckerElement(
                                alias, 
                                file_path, 
                                TerraformObjectType.REQUIRED_PROVIDER,
                                None,
                                {}
                                )
                    unique_id = uuid4()
                    self.extract[unique_id] = checker_element
                    self.checker_elements_ids[terraform_object_type].append(unique_id)

    def _read_provider(self, hcl_content: dict, terraform_object_type: TerraformObjectType, file_path: str):
        for provider_setup in hcl_content:
            provider_setup_name = list(provider_setup.keys())[0]
            checker_element = CheckerElement(
                                provider_setup_name, 
                                file_path, 
                                terraform_object_type,
                                None,
                                {}
                                )
            unique_id = uuid4()
            self.extract[unique_id] = checker_element
            self.checker_elements_ids[terraform_object_type].append(unique_id)

    def read(self, folder_path):
        tf_files_paths = self._get_tf_files_paths(folder_path)

        for file in tf_files_paths:
            hcl_file_content = self._get_hcl_content(file)
            for str_terraform_object_type in hcl_file_content.keys():
                if not str_terraform_object_type in TerraformObjectType:
                    logging.warning(f"{str_terraform_object_type} is not part of terracheck.types.TerraformObjectType enumeration. Not considered.")
                else:
                    terraform_object_type = TerraformObjectType(str_terraform_object_type)
                    if terraform_object_type in [TerraformObjectType.RESOURCE, TerraformObjectType.DATA]:
                        self._read_resource_data(hcl_file_content[terraform_object_type.value], terraform_object_type, file)
                    elif terraform_object_type in [TerraformObjectType.VARIABLE, TerraformObjectType.OUTPUT]:
                        self._read_variable_output(hcl_file_content[terraform_object_type.value], terraform_object_type, file)
                    elif terraform_object_type == TerraformObjectType.TERRAFORM:
                        self._read_terraform(hcl_file_content[terraform_object_type.value], terraform_object_type, file)
                    elif terraform_object_type == TerraformObjectType.PROVIDER:
                        self._read_provider(hcl_file_content[terraform_object_type.value], terraform_object_type, file)
                        
# hcl_checker_reader = HclCheckerReader()
# extract = hcl_checker_reader.read("/home/wattache/projects/terraform_checker/tests/hcl_sample_1")

# for element_type, checker_element in extract.items():
#     print(json.dumps(checker_element.to_dict(), indent=4))