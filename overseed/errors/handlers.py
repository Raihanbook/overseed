from flask import Blueprint, render_template

errors = Blueprint('errors', __name__)

# ERRORS
# ---------------
# We need to use the @app_errorhandler decorator instead of the 
# @route decorator.

# 404
# ---------------
# This page is for errors where a page cannot be found.
@errors.app_errorhandler(404)
def error_404(error):
    return render_template('errors/404.html'), 404

# 403
# ---------------
# This page is for errors where the user does not have appropriate permissions.
@errors.app_errorhandler(403)
def error_403(error):
    return render_template('errors/403.html'), 403

# 500
# ---------------
# This page is for when there is an internal server error.
@errors.app_errorhandler(500)
def error_500(error):
    return render_template('errors/500.html'), 500