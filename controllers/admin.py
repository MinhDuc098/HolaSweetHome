import random
import re
import string
from models.home import RoomDetail, RoomImage
from models.user import Bookmark, RoomRequest
from models.user import UserRole, User, HomeOwnerRequest, WebsiteFeedback
from models.model import db
from flask import Flask, redirect, url_for, json, render_template, request, session, flash
from flask_mail import Message
from controllers.mail_service import mail
from models.user import HomeOwnerRequest, User
from datetime import datetime
from models.post import Post, PostImage
from models.report import ReportPost, ReportHome, ReportUser, ReportUserDetail
from models.home import Home


def dashBoard():
    users = User.query.all()
    posts = Post.query.all()
    homes = Home.query.all()
    rooms = RoomDetail.query.all()
    return render_template('admin/dashBoard.html', users=users, posts=posts, homes=homes, rooms=rooms, user=User, post=Post, home=Home, reportedPosts=ReportPost, reportedHomes=ReportHome, reportedUsers=ReportUser)


def view_request_register():

    request_register = HomeOwnerRequest.query.all()
    return render_template("admin/view_request_register.html", request_register=request_register)


def allow_access():
    id = request.args.get("id")
    request_register = HomeOwnerRequest.query.filter_by(id=id).first()
    home_user = User.query.filter_by(id=request_register.user_id).first()
    home_user.banned = 0
    db.session.commit()
    request_register.status = True
    db.session.commit()
    msg = Message('Your request has been accepted. Your password is: ' + home_user.password,
                  sender='yenduls@gmail.com', recipients=[home_user.email])
    mail.send(msg)
    return redirect(url_for("admin_router.view_request_register"))


def reported_Posts():
    reported_posts = ReportPost.query.all()
    return render_template('admin/reportedPosts.html', posts=reported_posts)


def delete_report():
    report_id = request.form.get("id")
    report = ReportPost.query.filter_by(id=report_id).first()
    email = report.user.email
    if report:
        db.session.delete(report)
        db.session.commit()

        msg = Message('Refuse report',
                      sender='yenduls@gmail.com ', recipients=[email])
        msg.body = "Your report has been refuse by admin \r\n Reason: " + report.reason + \
            "\r\n Please contact admin for more information"
        mail.send(msg)

        return redirect(url_for('admin_router.reportedPosts'))
    return redirect(url_for('admin_router.reportedPosts'))


def accept_report():
    report_id = request.form.get("id")
    report = ReportPost.query.filter_by(id=report_id).first()
    emailReporter = report.user.email
    if report:
        db.session.delete(report)
        db.session.commit()

    postID = report.post_id
    post_img = PostImage.query.filter_by(post_id=postID).first()
    if post_img:
        # for img in post_img:
        db.session.delete(post_img)
        db.session.commit()

    post = Post.query.filter_by(id=postID).first()
    email = post.author.email
    if post:
        db.session.delete(post)
        db.session.commit()

        msg = Message('Accept report',
                      sender='yenduls@gmail.com ', recipients=[emailReporter])
        msg.body = "Your report has been accpted by admin \r\n Reason: " + report.reason + \
            "\r\n Please contact admin for more information"
        mail.send(msg)

        msg = Message('Delete post',
                      sender='yenduls@gmail.com ', recipients=[email])
        msg.body = "Your post has been delete by admin \r\n Reason: " + report.reason + \
            "\r\n Reason" + post.content + \
            "\r\n Please contact admin for more information"
        mail.send(msg)

        return redirect(url_for('admin_router.reportedPosts'))
    return redirect(url_for('admin_router.reportedPosts'))


def view_feedback():
    feedback_list = WebsiteFeedback.query.all()
    for feedback in feedback_list:
        feedback.username = User.query.filter_by(
            id=feedback.user_id).first().username
    return render_template("admin/view_feedback.html", feedback_list=feedback_list)


def all_Homes():
    homes = Home.query.all()
    return render_template('admin/allHomes.html', homes=homes)


def delete_home():
    homeID = request.form.get("id")
    rooms = RoomDetail.query.filter_by(home_id=homeID).all()
    if rooms:
        for room in rooms:
            image = RoomImage.query.filter_by(room_id=room.id).first()
            if image:
                db.session.delete(image)
                db.session.commit()
            db.session.delete(room)
            db.session.commit()

    home = Home.query.filter_by(id=homeID).first()
    email = home.owner.email
    if home:
        db.session.delete(home)
        db.session.commit()

        msg = Message('Your home has been deleted by admin',
                      sender='yenduls@gmail.com ', recipients=[email])
        msg.body = "Your post has been deleted by admin  \r\nPlease contact admin for more information"
        mail.send(msg)

        return redirect(url_for('admin_router.all_Homes'))
    return redirect(url_for('admin_router.all_Homes'))


def reported_Homes():
    reportedHomes = ReportHome.query.all()
    return render_template('admin/reportedHomes.html', reportedHomes=reportedHomes)


def delete_home_report():
    report_id = request.form.get("id")
    report = ReportHome.query.filter_by(id=report_id).first()
    email = report.user.email
    if report:

        msg = Message('Your report has been refuse',
                      sender='yenduls@gmail.com ', recipients=[email])
        msg.body = "Your report has been refused by admin  \r\nHome: " + report.home.name + "\r\nReason: " + \
            report.reason + "\r\nPlease contact admin for more information"
        mail.send(msg)

        db.session.delete(report)
        db.session.commit()
        return redirect(url_for('admin_router.reportedHomes'))
    return redirect(url_for('admin_router.reportedHomes'))


def accept_home_report():
    report_id = request.form.get("id")
    report = ReportHome.query.filter_by(id=report_id).first()
    emailReporter = report.user.email
    if report:
        db.session.delete(report)
        db.session.commit()

    homeID = report.home_id
    rooms = RoomDetail.query.filter_by(home_id=homeID).all()
    if rooms:
        for room in rooms:
            image = RoomImage.query.filter_by(room_id=room.id).first()
            if image:
                db.session.delete(image)
                db.session.commit()
            db.session.delete(room)
            db.session.commit()

    home = Home.query.filter_by(id=homeID).first()
    email = home.owner.email
    if home:

        msg = Message('Your report has been accepted',
                      sender='yenduls@gmail.com ', recipients=[emailReporter])
        msg.body = "Your report has been accepted by admin  \r\nHome: " + home.name + " is deleted\r\nReason: " + \
            report.reason + "\r\nPlease contact admin for more information"
        mail.send(msg)

        msg = Message('Your home has been deleted',
                      sender='yenduls@gmail.com ', recipients=[email])
        msg.body = "Your home has been reported and deleted by admin\r\nHome: " + home.name + "\r\nReason: " + \
            report.reason + "\r\nPlease contact admin for more information"
        mail.send(msg)

        db.session.delete(home)
        db.session.commit()
        return redirect(url_for('admin_router.reportedHomes'))
    return redirect(url_for('admin_router.reportedHomes'))


def all_Posts():
    posts = Post.query.all()
    return render_template('admin/allPosts.html', posts=posts)


def delete_post():
    postID = request.form.get("id")
    post_img = PostImage.query.filter_by(post_id=postID).first()
    if post_img:
        # for img in post_img:
        db.session.delete(post_img)
        db.session.commit()

    post = Post.query.filter_by(id=postID).first()
    email = post.author.email

    if post:
        db.session.delete(post)
        db.session.commit()

        msg = Message('Your post has been deleted by admin',
                      sender='yenduls@gmail.com ', recipients=[email])
        msg.body = "Your post has been deleted by admin, post content :" + \
            post.content + ", please contact admin for more information"
        mail.send(msg)

        return redirect(url_for('admin_router.all_Posts'))
    return redirect(url_for('admin_router.all_Posts'))


def all_Users():
    users = User.query.all()
    return render_template('admin/allUser.html', users=users)


def banned_Users():
    users = User.query.filter_by(banned=1).all()
    return render_template('admin/bannedUsers.html', users=users)


def ban_user():
    user_id = request.form.get("id")
    user = User.query.filter_by(id=user_id).first()
    email = user.email
    if user:
        user.banned = 1
        db.session.commit()

        msg = Message('You are banned by admin',
                      sender='sweethomehola@outlook.com', recipients=[email])
        msg.body = "You are banned by admin, please contact admin for more information"
        mail.send(msg)

        return redirect(url_for('admin_router.all_Users'))
    return redirect(url_for('admin_router.all_Users'))


def unban_user():
    user_id = request.form.get("id")
    user = User.query.filter_by(id=user_id).first()
    email = user.email
    if user:
        user.banned = 0
        db.session.commit()

        msg = Message('You are unbanned by admin',
                      sender='sweethomehola@outlook.com', recipients=[email])
        msg.body = "Contact admin for more information and to answer questions, have a nice day"
        mail.send(msg)

        return redirect(url_for('admin_router.banned_Users'))
    return redirect(url_for('admin_router.banned_Users'))


def unban_user2():
    user_id = request.form.get("id")
    user = User.query.filter_by(id=user_id).first()
    email = user.email
    if user:
        user.banned = 0
        db.session.commit()

        msg = Message('You are unbanned by admin',
                      sender='sweethomehola@outlook.com', recipients=[email])
        msg.body = "Contact admin for more information and to answer questions, have a nice day"
        mail.send(msg)

        return redirect(url_for('admin_router.all_Users'))
    return redirect(url_for('admin_router.all_Users'))


def reported_Users():
    reportedUsers = ReportUserDetail.query.all()
    return render_template('admin/reportedUsers.html', reportedUsers=reportedUsers)


def ban_report_user():
    report_id = request.form.get("id")
    reportDetail = ReportUserDetail.query.filter_by(
        reported_user_id=report_id).first()
    if reportDetail:
        db.session.delete(reportDetail)
        db.session.commit()

    report = ReportUser.query.filter_by(id=reportDetail.report_id).first()
    userReport = User.query.filter_by(id=report.reporter_id).first()
    emailUserReport = userReport.email
    if report:
        db.session.delete(report)
        db.session.commit()

    user_id = reportDetail.reported_user_id
    user = User.query.filter_by(id=user_id).first()
    email = user.email
    if user:
        user.banned = 1
        db.session.commit()

        msg = Message('You are banned by admin',
                      sender='sweethomehola@outlook.com', recipients=[email])
        msg.body = "You are banned by ademin, the reason is: " + \
            reportDetail.reason + ", please contact admin for more information"
        mail.send(msg)

        msg = Message('Accept report',
                      sender='sweethomehola@outlook.com', recipients=[emailUserReport])
        msg.body = "Your report is excuted, user :" + user.username + " is banned, the reason is: " + \
            reportDetail.reason + \
            ", thank you for your contribution, please contact admin for more information"
        mail.send(msg)

        return redirect(url_for('admin_router.reportedUsers'))
    return redirect(url_for('admin_router.reportedUsers'))
