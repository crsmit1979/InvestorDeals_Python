import config
import os
print("Changing config files to TEST")
script_path= os.path.dirname(os.path.abspath( __file__ ))
module_path = script_path

base_file = "%s\\%s" % (module_path, "config_base.json")
override_file = "%s\\%s" % (module_path, "config_test.json")

config.transform_files(base_file, override_file)