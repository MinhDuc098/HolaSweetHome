from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .chat import Chat, Message
from .home import Home, RoomImage, HomeReview, RoomDetail
from .report import ReportHome, ReportPost, ReportUser
from .user import Bookmark, RoomRequest, User, UserRole, WebsiteFeedback, HomeOwnerRequest
from .post import Post, Comment, PostImage, Upvote
