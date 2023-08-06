#!/usr/bin/env python

"""
Converts a YAML file into a JSON file.
"""

import sys
from json import dump
from yaml import safe_load

def main():
    """
    Reads a YAML file as input and saves a JSON file with the
    same basename (i.e. myfile.yml -> myfile.json)
    """

    # Get file name from command
    if len(sys.argv) == 2:
        yaml_file = sys.argv[1]
    else:
        msg = "Input file not specified!"
        raise FileNotFoundError(msg)

    # Open the YAML file
    with open(yaml_file, 'r', encoding='utf-8') as f:
        data = safe_load(f)

    # Write to JSON file
    json_file = yaml_file.replace('.yml', '.json')
    with open(json_file, 'w', encoding='utf-8') as f:
        dump(data, f, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    main()
