from pathlib import Path


def path(hex_name, n=1):
    folder_name = hex_name
    return Path("./assets/art/hexes") / folder_name / f"{hex_name}{n}.png"
