from models.Migration import Migrations
from datetime import datetime
import glob
from models.DealBase import dbase
import os
from db.db import initialize_db
import log

def script_loaded(name):
    return len(Migrations.select().where(Migrations.file == name)) > 0

def run_script(name):
    txt = ""
    with open(name, "r") as f:
        scripts = f.read().split('--script--')
        for script in scripts:
            if len(script) > 0:
                dbase.execute_sql(script)
                dbase.commit()
                log.log_normal(txt)
            else:
                log.log_normal("File got not sql scripts [%s]" % (name))
    Migrations.create(file=name, date_run=datetime.now())

def run_migration():
    if not os.path.exists("./deals.db"):
        log.log_normal("running database initialization")
        initialize_db()

    log.log_normal("running migration scripts")
    mypath = "./db/migration_scripts/*.sql"
    files = glob.glob(mypath)
    ordered_files = sorted(files)
    for item in ordered_files:
        if  script_loaded(item) == False:
            log.log_normal("Running Script [%s]" % (item))
            run_script(item)
        else:
            log.log_warning("Script already loaded [%s]" % (item))