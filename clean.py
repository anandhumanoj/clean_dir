#!/usr/bin/env python
import os
import re
import shutil
import argparse
import json
from random import Random

"""
A simple program to clean up your download directory
by #AnandhuManoj
Github https://github.com/anandhumanoj
#HAPPYCODING

"""
#  TODO :POSTPONED: add intelligent match for related files and folders
#  TODO : Add additional configuration for advanced topic based categorisation in inner directories

file_types = {}
file_types_un_formatted = {}
file_sizes = {}
fallback_dir = False
exp_ignore_files = {}
base_dir = ""
result = {}


def walk_through(path, run_method, is_recursive=False, run_always=False):
	"""
		Check through the directory
	:param path: Path to root folder
	:param run_method: method to run on each file should have a param accepting path
	:param is_recursive: Whether or not sub directories should be checked
	:param run_always: always call run_method on both files and dirs
	:return None:
	"""

	if path != "":
		for dirItem in os.listdir(path):
			if os.path.isdir(path + "/" + dirItem):
				if is_recursive:
					walk_through(path + "/" + dirItem, run_method)
				if run_always:
					run_method(dirItem, path)
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
	#  Ignore files given in config
	for regexp in exp_ignore_files:
		if re.match(regexp, file_item):
			return
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
		if fallback_dir:

			if fallback_dir not in result.keys():
				result[fallback_dir] = []
			result[fallback_dir].append(file_item)
			move_files(fallback_dir, file_item, dir_path)
			return

	except (OSError, IOError) as Err:
		print("Error While moving files")
		print(Err)
		exit(1)
	except KeyError as key_error:
		print("Invalid Keys in Configuration file")
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
	if (curr_file_destination != full_file_path):
		if os.path.exists(curr_file_destination):
			rand = Random()
			file_name = "(" + str(rand.randint(0, 9)) + ") - " + file_name
			curr_file_destination = full_dir + "/" + file_name
		shutil.move(full_file_path, curr_file_destination)


def parse_config(config_file):
	def convert_to_regexp(y):
		return "(.*" + re.escape(y) + "$)"

	try:
		with open(config_file, "r") as f_types:
			config_data = json.load(f_types)
			if "Categories" in config_data.keys():
				globals()['file_types_un_formatted'] = config_data['Categories']
			else:
				raise ValueError()
			if "Sizes" in config_data.keys():
				globals()['file_sizes'] = config_data['Sizes']
			else:
				raise ValueError()
			if "FallBackDir" in config_data.keys():
				globals()['fallback_dir'] = config_data['FallBackDir']
			if "IgnoreFiles" in config_data.keys():
				globals()['exp_ignore_files'] = config_data['IgnoreFiles']
	except ValueError as value_error:
		print("Invalid data file. Exiting...")
		print(value_error)
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


def arg_parse():
	parser = argparse.ArgumentParser("A simple program to clean up your download directory")
	parser.add_argument("--dir", nargs="?", default="", const="", help="Directory to run against")
	parser.add_argument("--config", nargs="?", default="", const="",
						help="JSON file in predefined format to sort files by its extension")

	parser.add_argument("-r", "--recursive", type=bool, nargs="?", const=True, help="Recursively Scan sub directories",
						default=False)
	parser.add_argument("-c", "--clean", type=bool, nargs="?", const=True,
						help="Clean empty directories created after categorisation",
						default=False)
	parser.add_argument("-a", "--all", type=bool, nargs="?", const=True, help="Scan all files (. files too)",
						default=False)
	parser.add_argument("-d", "--default", type=bool, nargs="?", const=True,
						help="Work with default folder (~/Downloads folder)",
						default=False)
	parser.add_argument("-v", '--verbose', type=bool, nargs="?", default=False, const=True, help="Show files scanned")
	return parser.parse_args()


def clean_empty_dir(item_name, path):
	dir_item = path + "/" + item_name
	try:
		if os.path.isdir(dir_item):
			if len(os.listdir(dir_item)) == 0:
				os.rmdir(dir_item)
				if args.verbose:
					print(dir_item + " removed")
			else:
				pass
		else:
			pass
	except (OSError, IOError) as error:
		print(error)
		print("Skipping current directory")


def main():
	global args
	args = arg_parse()
	host_dir = os.path.abspath(os.path.dirname(__file__))
	config_file = host_dir + "/config.json"
	if args.config != "":
		config_file = args.config
	parse_config(config_file)
	if not args.all:
		globals()['exp_ignore_files'].insert(0, u"^\..*")
	if args.dir != "" and os.path.isdir(args.dir):
		globals()['base_dir'] = args.dir
	elif args.default:
		globals()['base_dir'] = os.path.expanduser("~") + "/Downloads"
	else:
		print(args.dir + " is not a directory. Exiting...")
		exit(1)
	if args.verbose:
		print("Scanning  " + base_dir)
	walk_through(base_dir, find_files, is_recursive=args.recursive)
	if args.clean:
		if args.verbose:
			print("Scanning for Empty directories...")
		walk_through(base_dir, clean_empty_dir, is_recursive=args.recursive, run_always=True)
	if args.verbose:
		file_count = 0
		for cat, files in result.items():
			print("+" + cat)
			for file in files:
				print("-" + file)
				file_count = file_count + 1
		print("--------------")
		print(str(file_count) + " files moved ")


if __name__ == '__main__':
	main()
