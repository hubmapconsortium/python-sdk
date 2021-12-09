#!/usr/bin/env python

import argparse
import json
import os
from typing import Any, Dict, List, Optional, Union


class RawTextArgumentDefaultsHelpFormatter(
    argparse.ArgumentDefaultsHelpFormatter,
    argparse.RawTextHelpFormatter
):
    pass


# https://docs.python.org/3/howto/argparse.html
parser = argparse.ArgumentParser(
    description='Rebuild the python-sdk from the constituent openapi specs.\n'
                'If no argument given then all will be built if arguments are given then only build those',
    formatter_class=RawTextArgumentDefaultsHelpFormatter)
parser.add_argument('modules', nargs='*',
                    help='name of the modules to rebuild')
parser.add_argument("-s", "--sources", type=str, default='./sources.json',
                    help='file containing the sources for the openapi specs')
parser.add_argument("-v", "--verbose", action="store_true",
                    help='run with verbose output')

args = parser.parse_args()

sources = json.load(open(args.sources, 'r'))
modules_to_build = [s.lower() for s in args.modules]
all_modules = list(sources.keys())

if len(modules_to_build) > 0:
    for module in modules_to_build:
        if module not in all_modules:
            print(f"ERROR... Module name '{module}' not found in '{args.sources}'")
            exit(1)
else:
    modules_to_build = all_modules

if args.verbose is True:
    print(f'Building modules: {modules_to_build}')

for module in modules_to_build:
    if args.verbose is True:
        print(f"*** Downloading: {sources[module]['openapi-url']}")
    os.system(f"wget -O ./api-spec.yaml {sources[module]['openapi-url']}")
    if args.verbose is True:
        print(f"*** Generating: {module}")
    action = 'generate'
    # https://pypi.org/project/openapi-python-client/
    os.system(f"openapi-python-client {action} --path ./api-spec.yaml")
    module_dash = module.replace('-', '_')
    os.system(f"mv hu-bmap-{module}-client/hu_bmap_{module_dash}_client hubmap_sdk")
    os.system(f"mv ./api-spec.yaml hubmap_sdk/hu_bmap_{module_dash}_client")
    os.system(f"rm -rf hu-bmap-{module}-client")
