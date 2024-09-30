import os

from importlib.machinery import SourceFileLoader
original_path = os.path.dirname(os.path.abspath(__file__))
top_one_path  = original_path[:-5]

outside = SourceFileLoader("", top_one_path+"utils\\utility\\testing_import_from_another_folder_in_top_root.py").load_module()
outside.mine()
cMine = outside.Mine
print("Dibawah")
cMine()
# foo.mine()


# from ..testing_import_from_top_root import mine
# mine()