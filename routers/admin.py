
import controllers.user
import controllers.admin
from decorators.authentication import login_required, admin_required
from flask import Blueprint, jsonify, request, render_template, session
from models.user import UserRole, User
from models.post import Post

admin_router = Blueprint('admin_router', __name__)


@admin_router.route("/dashBoard")
@admin_required
def dashBoard():
    return controllers.admin.dashBoard()


@admin_router.route('/view_request_register', methods=['POST', 'GET'])
def view_request_register():
    return controllers.admin.view_request_register()


@admin_router.route('/allow_access', methods=["Post", "get"])
def allow_access():
    return controllers.admin.allow_access()


@admin_router.route("/refuse_access", methods=['POST', 'GET'])
def refuse_access():
    return controllers.admin.refuse_access()


@admin_router.route("/reportedPosts")
@admin_required
def reportedPosts():
    return controllers.admin.reported_Posts()


@admin_router.route('/delete_report', methods=["POST", "GET"])
@admin_required
def delete_report():
    if request.method == "POST":
        return controllers.admin.delete_report()


@admin_router.route('/accept_report', methods=["POST", "GET"])
@admin_required
def accept_report():
    if request.method == "POST":
        return controllers.admin.accept_report()


@admin_router.route('/view_feedback', methods=["GET"])
@admin_required
def view_feedback():
    return controllers.admin.view_feedback()


@admin_router.route("/all_Homes")
@admin_required
def all_Homes():
    return controllers.admin.all_Homes()


@admin_router.route('/delete_home', methods=["POST", "GET"])
@admin_required
def delete_home():
    if request.method == "POST":
        return controllers.admin.delete_home()


@admin_router.route("/reportedHomes")
@admin_required
def reportedHomes():
    return controllers.admin.reported_Homes()


@admin_router.route('/delete_home_report', methods=["POST", "GET"])
@admin_required
def delete_home_report():
    if request.method == "POST":
        return controllers.admin.delete_home_report()


@admin_router.route('/accept_home_report', methods=["POST", "GET"])
@admin_required
def accept_home_report():
    if request.method == "POST":
        return controllers.admin.accept_home_report()


@admin_router.route("/all_Posts")
@admin_required
def all_Posts():
    return controllers.admin.all_Posts()


@admin_router.route("/delete_post", methods=["POST", "GET"])
@admin_required
def deleta_post():
    if request.method == "POST":
        return controllers.admin.delete_post()


@admin_router.route("/all_Users")
@admin_required
def all_Users():
    return controllers.admin.all_Users()


@admin_router.route("/banned_Users")
@admin_required
def banned_Users():
    return controllers.admin.banned_Users()


@admin_router.route('/ban_user', methods=["POST", "GET"])
@admin_required
def ban_user():
    if request.method == "POST":
        return controllers.admin.ban_user()


@admin_router.route('/unban_user', methods=["POST", "GET"])
@admin_required
def unban_user():
    if request.method == "POST":
        return controllers.admin.unban_user()


@admin_router.route('/unban_user2', methods=["POST", "GET"])
@admin_required
def unban_user2():
    if request.method == "POST":
        return controllers.admin.unban_user2()


@admin_router.route("/reportedUsers")
@admin_required
def reportedUsers():
    return controllers.admin.reported_Users()


@admin_router.route("/banReportedUser", methods=["POST", "GET"])
@admin_required
def ban_report_user():
    if request.method == "POST":
        return controllers.admin.ban_report_user()
