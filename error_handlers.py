import log
from flask import render_template

def apply_error_handlers(app=None):
    @app.errorhandler(403)
    def internal_server_error_403(error):
        log.log_error('Server Error: %s' % (error))
        return render_template('error.htm', msg="403"), 403

    @app.errorhandler(404)
    def internal_server_error_404(error):
        log.log_error('Server Error: %s' % (error))
        return render_template('error.htm', msg="404"), 404

    @app.errorhandler(410)
    def internal_server_error_410(error):
        log.log_error('Server Error: %s' % (error))
        return render_template('error.htm', msg="410"), 410

    @app.errorhandler(500)
    def internal_server_error_500(error):
        log.log_error('Server Error: %s' % (error))
        return render_template('error.htm', msg="500"), 500

    @app.errorhandler(Exception)
    def unhandled_exception(e):
        log.log_error('Unhandled Exception: %s' % (e))
        import sys
        import traceback
        msg = ''.join(traceback.format_tb(e.__traceback__))
        log.log_error(msg)
        return render_template('error.htm', msg="unknown"), 500

