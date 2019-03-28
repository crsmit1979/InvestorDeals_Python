import os
import json

def module_path():
    script_path = os.path.dirname(os.path.abspath(__file__))
    return script_path


def read_json(nm):
    txt = {}
    with open(nm) as f:
        txt = f.read()

    return json.loads(txt)


def get_config(name):
    file = "%s\\%s" % (module_path(), "config.json")
    json = read_json(file)
    return json[name]


def transform_files(base_file, override_file):
    base = read_json(base_file)
    override = read_json(override_file)

    for name in override:
        base[name] = override[name]

    save_file = "%s\\%s" % (module_path(), "config.json")
    print("Saving Transformed Config file [%s] " % (save_file))
    print("Transformed config content: %s" % (base))
    with open(save_file, 'w') as fp:
        json.dump(base, fp, indent=4)


def transform(environment):
    print("transform: "+ module_path())
    base_file = "%s\\%s" % (module_path(), "config_base.json")

    override = ""
    if environment == "TEST":
        override = "%s\\%s" % (module_path(), "config_test.json")
    if environment == "PROD":
        override = "%s\\%s" % (module_path(), "config_prod.json")

    transform_files(base_file, override)