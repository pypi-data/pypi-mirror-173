import re
from typing import List


def find(inputs: str, sequence: str) -> List:
    return [r.span() for r in re.finditer(inputs, sequence)]
