#!/usr/bin/env python
import os
import re
import shutil
import argparse
import json

"""
A simple program to clean up your download directory
by #AnandhuManoj
Github https://github.com/anandhumanoj
#FUNNYCODE_DAY|01|02

"""
#  TODO: add intelligent match for related files and folders

file_types = {}
file_types_un_formatted = {}
file_sizes = {}
base_dir = ""
result = {}


def walk_through(path, run_method, is_recursive=False):
    """
        Check through the directory
    :param path: Path to root folder
    :param run_method: method to run on each file should have a param accepting path
    :param is_recursive: Whether or not sub directories should be checked
    :return None:
    """

    if path != "":
        for dirItem in os.listdir(path):
            if os.path.isdir(path + "/" + dirItem):
                if is_recursive:
                    walk_through(path + "/" + dirItem, run_method)
            else:
                run_method(dirItem, path)

        return None


def find_files(file_item, dir_path):
    """
    Used to find files of certain type as given in @var,file_types
    :param file_item:
    :param dir_path
    :return none:
    """
    file_path = dir_path + "/" + file_item
    #  To find files with file_sizes constraint
    try:
        for category, types in file_sizes.items():
            for file_cat in types['file_cats']:

                match = file_types[file_cat]
                min_file_size = (types['min_size']) * 1024 * 1024  # Convert file_size:MiB => bytes
                if re.match(match, file_item) and os.path.getsize(file_path) >= min_file_size:
                    if category not in result.keys():
                        result[category] = []
                    result[category].append(file_item)
                    move_files(category, file_item, dir_path)
                    return
        #  To find files with file_types constraint
        for category, match in file_types.items():
            if re.match(match, file_item):
                if category not in result.keys():
                    result[category] = []
                result[category].append(file_item)
                move_files(category, file_item, dir_path)
                return
    except (OSError, IOError) as Err:
        print("Error While moving files")
        print(Err)
        exit(1)
    except KeyError as key_error:
        print("Invalid Key in json_sizes.json")
        print(key_error)
        exit(1)



def move_files(category, file_name, dir_name):
    """
    Move files to specified folders

    :param file_name: Name of the file to move
    :param dir_name: directory containing the file
    :param category: category of the file
    :rtype: None
    """
    global base_dir
    full_dir = base_dir + "/" + category
    full_file_path = dir_name + "/" + file_name
    curr_file_destination = full_dir + "/" + file_name
    if not os.path.isdir(full_dir):
        os.mkdir(full_dir)
    if not os.path.isfile(curr_file_destination):
        shutil.move(full_file_path, curr_file_destination)


def parse_file_types():
    def convert_to_regexp(y):
        return "(.*" + re.escape(y) + "$)"

    host_dir = os.path.abspath(os.path.dirname(__file__))
    try:

        with open(host_dir + "/file_types.json", "r") as f_types:
            globals()['file_types_un_formatted'] = json.load(f_types)

        with open(host_dir + "/file_sizes.json", "r") as f_sizes:
            globals()['file_sizes'] = json.load(f_sizes)

    except ValueError:
        print("Invalid data file(s). Exiting...")
        exit(1)
    except (OSError, IOError) as Err:

        print("Data file " + Err.filename + " Not found. Exiting...")
        exit(1)

    finally:
        for category, file_list in file_types_un_formatted.items():
            str_regexp = ""
            for file_type in file_list.split(","):
                str_regexp += "|" + convert_to_regexp(file_type)
            file_types[category] = str_regexp.strip('|')


def main():
    parse_file_types()
    parser = argparse.ArgumentParser("A simple program to clean up your download directory")
    parser.add_argument("--dir", nargs="?", default="", const="", help="Directory to run against")
    parser.add_argument("-r", "--recursive", type=bool, nargs="?", const=True, help="Recursively Scan sub directories",
                        default=False)
    parser.add_argument("-d", "--default", type=bool, nargs="?", const=True,
                        help="Work with default folder (~/Downloads folder)",
                        default=False)
    parser.add_argument("-v", '--verbose', type=bool, nargs="?", default=False, const=True, help="Show files scanned")
    args = parser.parse_args()
    if args.dir != "" and os.path.isdir(args.dir):
        globals()['base_dir'] = args.dir
    elif args.default:
        globals()['base_dir'] = os.environ['HOME'] + "/Downloads"
    else:
        print(args.dir + " not a valid directory. Exiting...")
        exit(2)
    if args.verbose:
        print("Current Directory is " + base_dir)

    walk_through(base_dir, find_files, is_recursive=args.recursive)
    if args.verbose:
        for cat, files in result.items():
            print("+" + cat)
            for file in files:
                print("-" + file)


if __name__ == '__main__':
    main()
