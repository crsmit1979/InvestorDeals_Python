print("Changing config files to PROD")
import config
import os
script_path= os.path.dirname(os.path.abspath( __file__ ))
module_path = script_path

base_file = "%s\\%s" % (module_path, "config_base.json")
override_file = "%s\\%s" % (module_path, "config_prod.json")

config.transform_files(base_file, override_file)