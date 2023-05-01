from pathlib import Path


def path(hex_name, n=1):
    folder_name = hex_name
    return Path("./assets/art/hexes") / folder_name / f"{hex_name}{n}.png"


def modifier_path(mod_name, n=None):
    alter_num_str = str(n) if n is not None else ""
    return Path("./assets/art/modifiers") / mod_name / f"{mod_name}{alter_num_str}.png"