from email import message
import random
import string
from models.report import ReportUser, ReportUserDetail
from models.user import Bookmark, RoomRequest
from models.user import UserRole, User, HomeOwnerRequest, WebsiteFeedback
from models.model import db
from flask import Flask, redirect, url_for, json, render_template, request, session, flash
from flask_mail import Message
from controllers.mail_service import mail
from models.post import Post
from datetime import datetime


def home():
    if "username" in session:
        user = session['username']
        return render_template("user/home.html", username=user, isLogin=True)
    else:
        return render_template("user/home.html", stringName="you are not login", isLogin=False)


def login():
    user_name = request.form["user"]
    pass_word = request.form["pass"]
    query = User.query.filter(
        User.username == user_name, User.password == pass_word).first()
    if not query:
        flash("Your account doesn't exist", "info")
        return render_template("user/login.html")
    if query.banned == True:
        flash("You are banned!", "info")
        return render_template("user/login.html")
    if query:
        session['username'] = query.username
        session['id'] = query.id
        session['role'] = query.role
        session['banned'] = query.banned
        session['email'] = query.email
        return redirect(url_for("user_router.home"))
    return render_template("user/login.html")


def logout():
    session.clear()
    return redirect(url_for('user_router.home'))


def forgot_password(email):
    # kiem tra email
    user = db.session.execute(
        db.select(User).where(User.email == email)).first()
    if user != None:
        # gen new password
        new_password = gen_new_password()
        # update password
        user[0].password = new_password
        # luu password moi vao database
        db.session.commit()
        # send email
        msg = Message('Your new password is: ' + new_password,
                      sender='sweethomehola@outlook.com', recipients=[email])
        mail.send(msg)

        # thong bao toi front end
        flash("New password has been sent to your email.", "info")
        return render_template("user/login.html")
    else:
        flash("Wrong email!", "info")
        return render_template("user/forgot_password.html")


def check_exist_user(username, email):
    user = db.session.execute(db.select(User).where(
        User.username == username)).first()
    if user:
        return True
    user = db.session.execute(
        db.select(User).where(User.email == email)).first()
    if user:
        return True
    return False


def register(username, password, email):
    # kiem tra du lieu
    if not check_exist_user(username, email):
        # add vao database
        user = User(username=username, password=password, email=email)
        db.session.add(user)
        db.session.commit()
        session['username'] = user.username
        session['id'] = user.id
        session['role'] = user.role
        session['banned'] = user.banned
        session['email'] = user.email
        return redirect(url_for('user_router.home'))
    else:
        flash("duplicate email or username", "info")
        return render_template("user/register.html")


def register_seller(username, email, address, home_name):
    # kiem tra du lieu
    if not check_exist_user(username, email):
        password = gen_new_password()
        # add vao database
        user = User(username=username, email=email,
                    password=password, banned=True, role=UserRole.SELLER)
        db.session.add(user)
        db.session.commit()
        user = User.query.filter(User.username == username).first()

        user_request = HomeOwnerRequest(user_id=user.id, home_id=1)
        db.session.add(user_request)
        db.session.commit()

        session['username'] = user.username
        session['id'] = user.id
        session['role'] = user.role
        session['banned'] = False
        session['clear'] = True
        flash("Your request has been sent to admin. Please wait for approval, we will send password in your email. Now please add home!", "info")
        return render_template("home/add_home_for_owner.html", address=address, home_name=home_name)
    else:
        flash("duplicate email or username", "info")
        return render_template("user/register_seller.html")


def gen_new_password():
    password = ''
    for i in range(8):
        password += random.choice(string.ascii_letters +
                                  string.digits + string.punctuation)
    return password


def profile(username):
    user = User.query.filter(User.username == username).first()
    if user:
        email = user.email
        return render_template("user/userProfile.html", user=user, email=email)
    else:
        return render_template("user/userProfile.html", message="User not found")


def edit_profile():
    user = User.query.filter(User.id == session['id']).first()
    checkUsername = User.query.filter(
        User.username == request.form["username"]).first()
    if checkUsername:
        flash("Username already exists!", "info")
        return render_template("editProfile.html", username=user.username, email=user.email)
    checkEmail = User.query.filter(User.email == request.form["email"]).first()
    if checkEmail:
        flash("Email already exists!", "info")
        return render_template("editProfile.html", username=user.username, email=user.email)
    user.username = request.form["username"] if request.form["username"] != "" else user.username
    session['username'] = user.username
    user.email = request.form["email"] if request.form["email"] != "" else user.email
    db.session.commit()
    # return render_template("userProfile.html",username=user.username,email=user.email)
    return redirect(url_for('user_router.profile'))


def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author_id=user.id)\
        .order_by(Post.timestamp.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)


def bookmark(userid):
    bookmarks = Bookmark.query.filter(User.id == userid).all()
    # missing liked posts
    if bookmarks:
        return render_template("user/bookmark.html", bookmarks=bookmarks)
    flash("You don't have any bookmark yet!", "info")
    return render_template("user/bookmark.html")


def report(username):
    user = User.query.filter(User.username == username).first()
    if user:
        return render_template("user/report_user.html", username=username)
    else:
        return render_template("user/report_user.html", message="User not found")


def do_report(reported, reporter_id, reason):
    user = User.query.filter(User.username == reported).first()
    if user:
        report = ReportUser(reporter_id=reporter_id)
        db.session.add(report)
        reports = ReportUser.query.filter(reporter_id == reporter_id)
        report = reports[-1]
        reportDetail = ReportUserDetail(\
            report_id=report.id, reported_user_id=user.id,timestamp=datetime.now() ,reason=reason if reason != "" else "No reason")
        db.session.add(reportDetail)
        db.session.commit()
        return render_template("user/report_user.html", message="Report successfully!")
    else:
        return render_template("user/report_user.html", message="User not found")


def add_feedback(id, content):
    feedback = WebsiteFeedback(
        user_id=id, timestamp=datetime.now(), feedback=content)
    db.session.add(feedback)
    db.session.commit()
    return redirect(url_for('user_router.home'))
