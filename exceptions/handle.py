import werkzeug.exceptions
from flask import Blueprint, render_template

error_router = Blueprint('error', __name__)


@error_router.app_errorhandler(werkzeug.exceptions.NotFound)
def handle_not_found(e):
    return render_template('exceptions/exception.html', error=404, message="Not Found"), 404


@error_router.app_errorhandler(werkzeug.exceptions.InternalServerError)
def handle_internal_server_error(e):
    return render_template('exceptions/exception.html', error=500, message="Internal Server Error"), 500


@error_router.app_errorhandler(werkzeug.exceptions.BadRequest)
def handle_bad_request(e):
    return render_template('exceptions/exception.html', error=400, message="Bad Request"), 400


@error_router.app_errorhandler(werkzeug.exceptions.MethodNotAllowed)
def handle_method_not_allowed(e):
    return render_template('exceptions/exception.html', error=405, message="Method Not Allowed"), 405


@error_router.app_errorhandler(werkzeug.exceptions.RequestTimeout)
def handle_request_timeout(e):
    return render_template('exceptions/exception.html', error=408, message="Request Timeout"), 408
