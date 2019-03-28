from werkzeug.utils import secure_filename
from flask import Blueprint, request, send_from_directory, redirect, render_template
from config import config
import uuid
import os
import datetime
import pathlib
from flask_login import login_required, current_user
from BatchCSV import BatchCSV

def add_routes(app=None):
    upload_page = Blueprint('upload_page', __name__,
                            template_folder='templates')


    @upload_page.route("/sample_csv", methods=['GET'])
    def sample_csv():
        return send_from_directory(directory=".",
                                   filename="sample.csv",
                                   mimetype="text/csv",
                                   as_attachment=True,
                                   attachment_filename="sample.csv")

    @upload_page.route("/upload_csv", methods=['GET','POST'])
    def upload_csv():
        if request.method == 'POST':
            file = request.files['file']
            # if user does not select file, browser also
            # submit a empty part without filename
            newfilename = None
            if file:
                filename = secure_filename(file.filename)
                extension = pathlib.Path(filename).suffix
                newfilename = str(uuid.uuid4()) + extension
                file.save(os.path.join(config.get_config('UPLOAD_FOLDER_CSV_DOCUMENT'), newfilename))
                csv_file = os.path.join(config.get_config('UPLOAD_FOLDER_CSV_DOCUMENT'), newfilename)
                batch = BatchCSV.create(
                    Filename=newfilename,
                    Uploaded_By=current_user.uuid,
                    Upload_Date=datetime.datetime.now()
                    )

            return redirect("/add_deals_2/list")
        else:
            return render_template("upload_csv.html")

    app.register_blueprint(upload_page)
