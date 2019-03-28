from flask import url_for
import os
import datetime


def apply(app=None):
    def dated_url_for(endpoint, **values):
        if endpoint == 'static':
            filename = values.get('filename', None)
            if filename:
                file_path = os.path.join(app.root_path,
                                         endpoint, filename)
                values['q'] = int(os.stat(file_path).st_mtime)
        return url_for(endpoint, **values)


    @app.context_processor
    def override_url_for():
        return dict(url_for=dated_url_for)

    @app.context_processor
    def utility_processor():
        def time_ago(date):
            d1 = date
            d2 = datetime.datetime.now()

            daysDiff = (d2 - d1).days
            minutes= daysDiff * 24 * 60


            if (minutes < 1):
                    return "A few seconds ago"
            else:
                if (minutes < 10):
                    return "A few minutes ago"
                else:
                    if (minutes <= 60):
                        return "An hour ago"
                    else:
                        if (minutes <= 3*24*60):
                            return "A few days ago"
                        else:
                            return date.strftime("%d/%m/%Y")
        return dict(time_ago=time_ago)
