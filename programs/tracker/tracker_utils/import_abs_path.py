import os
from importlib.machinery import SourceFileLoader
original_path = os.path.dirname(os.path.abspath(__file__))
top_one_path  = original_path[:-len("tracker\\tracker_utils")]

print(f"Original path tracker: {original_path}")
print(f"Top one path tracker: {top_one_path}")

def import_outside_utils(outside_folder, file_name):
    return SourceFileLoader("", top_one_path + outside_folder + file_name).load_module()