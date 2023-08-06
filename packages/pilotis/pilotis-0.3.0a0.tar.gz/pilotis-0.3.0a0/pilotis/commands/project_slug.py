import re

_slug_forbidden_char = '[_ ]'


def slugify(project_name: str) -> str:
    lowered_name = project_name.lower()
    return re.sub(_slug_forbidden_char, '-', lowered_name)
