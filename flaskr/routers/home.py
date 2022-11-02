from decorators.authentication import login_required, admin_required, seller_required
from flask import Blueprint, jsonify, request, render_template, session, url_for, flash, redirect
from controllers import home
import controllers.home

home_router = Blueprint('home_router', __name__)


@home_router.route('/add_home', methods=["POST", "GET"])
@seller_required
def add_home():
    if request.method == "POST":
        return controllers.home.add_home()
    return render_template("home/add_home_for_owner.html")


@home_router.route('/load_home', methods=["POST", "GET"])
@seller_required
def load_home():
    return controllers.home.load_home()

@home_router.route('/remove_home',methods = ["POST","GET"])
@seller_required
def remove_home():
    return controllers.home.remove_home()


@home_router.route('/load_room', methods=["POST", "GET"])
@seller_required
def load_room():
    return controllers.home.load_room()

@home_router.route('/remove_room',methods = ["POST","GET"])
@seller_required
def remove_room():
    return controllers.home.remove_room()


@home_router.route('/add_room', methods=["Get", "POST"])
@seller_required
def add_room():
    home_id = request.args.get('home_id')
    if home_id == None:
        return redirect(url_for('home_router.load_home'))
    if request.method == "POST":
        return controllers.home.add_room()
    return render_template("home/add_room.html", home_id=home_id)

@home_router.route('/')
@login_required
def list_home():
    return controllers.home.list_home()


@home_router.route('/home_detail', methods=["GET"])
@login_required
def home_detail():
    home_id = request.args.get('home_id')
    return controllers.home.home_detail(home_id)


@home_router.route('/report/<int:home_id>', methods=["GET", "POST"])
@login_required
def report(home_id):
    return controllers.home.report(home_id=home_id)

@home_router.route('/do_report', methods=["POST"])
@login_required
def do_report():
    return controllers.home.do_report(request.form.get("home_id"), request.form.get("user_id") ,request.form.get("reason"))
@home_router.route('/search', methods=["GET", "POST"])
@login_required
def search():
    if request.method == "POST" and request.form.get("home_name") != None:
        return controllers.home.search(request.form.get("home_name"))
    return render_template("home/search_home.html")


@home_router.route('/compare', methods=["GET"])
@login_required
def compare():
    return controllers.home.compare(request.args.get("home1"), request.args.get("home2"))

@home_router.route('/home_compare', methods=["GET"])
@login_required
def home_compare():
    home_id = request.args.get('home_id')
    return controllers.home.home_compare(home_id)

