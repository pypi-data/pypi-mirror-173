from enum import Enum

from colorama import Style

from terracheck.types import RuleCategory

class CheckerIssue():

    def __init__(self, checking_category: RuleCategory.RuleCategory, message: str) -> None:
        self.checking_category     = checking_category.value
        self.message               = message

    def __str__(self) -> str:
        return f"[{self.checking_category[1]}{self.checking_category[0]}{Style.RESET_ALL}]: {self.message}"