from asyncio import start_server
import os
from uuid import uuid4

from terracheck.utils.utils import read_yaml, get_tf_files_paths
from terracheck.types.CheckerIssue import CheckerIssue
from terracheck.types.RuleCategory import RuleCategory
from terracheck.types.TerraformBasicFileName import TerraformBasicFileName

class StructureChecker():

    def __init__(self, yaml_config_file_path: str) -> None:
        self.report = {}
        self.config = read_yaml(yaml_config_file_path)

    def _check_files_presence(self, hcl_folder_path: str):
        for file_type, available_denominations in self.config["mandatory_files"].items():
            is_present = True
            for filename in available_denominations:
                is_present = os.path.isfile(os.path.join(hcl_folder_path, filename))
                if is_present:
                    break
            if not is_present:
                self.report[uuid4()] = CheckerIssue(
                    RuleCategory.MISSING_FILE,
                    f"File '{file_type}' is missing in your terraform folder. Available denominations : {available_denominations}."
                )

    def _check_filenames_nomenclature(self, hcl_folder_path: str):
        if "filenames_nomenclature" in self.config:
            all_tf_files_paths = get_tf_files_paths(hcl_folder_path)
            all_tf_files_names = [os.path.basename(path) for path in all_tf_files_paths]
            files_to_check = list(set(all_tf_files_names)- set([tbfn.value for tbfn in TerraformBasicFileName]))
            for filename in files_to_check:
                startswith_constraint = self.config["filenames_nomenclature"].get("startswith", "")
                if not filename.replace('.tf', '').startswith(startswith_constraint):
                    self.report[uuid4()] = CheckerIssue(
                        RuleCategory.FILENAME_CONSTRAINT,
                        f"File '{filename}' does not respect constraint 'startswith {startswith_constraint}'."
                    ) 
                endswith_constraint = self.config["filenames_nomenclature"].get("endswith", "")
                if not filename.replace('.tf', '').endswith(startswith_constraint):
                    self.report[uuid4()] = CheckerIssue(
                        RuleCategory.FILENAME_CONSTRAINT,
                        f"File '{filename}' does not respect constraint 'endswith {endswith_constraint}'."
                    ) 
                contains_constraint = self.config["filenames_nomenclature"].get("contains", "")
                if not contains_constraint in filename.replace('.tf', ''):
                    self.report[uuid4()] = CheckerIssue(
                        RuleCategory.FILENAME_CONSTRAINT,
                        f"File '{filename}' does not respect constraint 'contains {contains_constraint}'."
                    ) 


        

    def check(self, hcl_folder_path: str):
        
        self._check_files_presence(hcl_folder_path)
        self._check_filenames_nomenclature(hcl_folder_path)

        for id, issue in self.report.items():
            print(issue)
