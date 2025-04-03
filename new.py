from datetime import datetime, timedelta
import razorpay
from flask import request, jsonify
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from flask import Flask
from flask import request, session, make_response
from pymongo import MongoClient
from flask import Flask, request, jsonify, send_file, render_template
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
from flask_bcrypt import Bcrypt
from flask_cors import CORS
import datetime
from datetime import datetime
import random
import json
from email.mime.text import MIMEText
import smtplib
import uuid
import re
import os
import requests
from io import BytesIO
import subprocess
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import threading
import multiprocessing
import time
import zipfile
import requests
import base64
import threading
from fpdf import FPDF
from num2words import num2words

# from docx import Document
# from docx.shared import Pt
# from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
import subprocess

# --------------------------------------------------------------------------------

file_dir = "/home/bnbdevelopers-files/htdocs/files.bnbdevelopers.in/exam_files/"
files_url = "https://files.bnbdevelopers.in"
files_base_dir = "/home/bnbdevelopers-files/htdocs/files.bnbdevelopers.in/"
files_base_url = "https://files.bnbdevelopers.in/exam_files/"

# file_dir = "/home/mcfcamp-files/htdocs/files.mcfcamp.in/mcf_files/"
# files_url = "https://files.mcfcamp.in"
# files_base_dir = "/home/mcfcamp-files/htdocs/files.mcfcamp.in/"
# files_base_url = "https://files.mcfcamp.in/mcf_files/"

# ----------------------------------------------------------------------------------


app = Flask(__name__)
CORS(app)

client_monogo = MongoClient(
    'mongodb+srv://bnbdevs:feLC7m4jiT9zrmHh@cluster0.fjnp4qu.mongodb.net/?retryWrites=true&w=majority')
app.config['MONGO_URI'] = 'mongodb+srv://bnbdevs:feLC7m4jiT9zrmHh@cluster0.fjnp4qu.mongodb.net/?retryWrites=true&w=majority'

# client = MongoClient(
#     'mongodb+srv://mcfcamp:mcf123@mcf.nyh46tl.mongodb.net/')
# app.config['MONGO_URI'] = 'mongodb+srv://mcfcamp:mcf123@mcf.nyh46tl.mongodb.net/'

app.config['SECRET_KEY'] = 'a6d217d048fdcd227661b755'
db = client_monogo['patrakar_bhavan_db']
# db2 = client['students_exam_answers']
bcrypt = Bcrypt(app)
# login_manager = LoginManager(app)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = "ic2023wallet@gmail.com"
app.config['MAIL_PASSWORD'] = "irbnexpguzgxwdgx"


pch_bookings_db = client_monogo['hall_booking_conf']
pch_bookings_collection = pch_bookings_db['bookings']

logs_collection = pch_bookings_db["logs"]

host = ""


# notificationFlag = True

# def getNotfStat():
#     settings_db = db['count_db']
#     data = settings_db.find_one({"found":"2"})
#     if data :
#         notificationFlag=data['status']
#     else:
#         notificationFlag="on"
#     print("Notification - ",notificationFlag)
#     return notificationFlag


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/home')
def home():
    return 'home page'

# -------------- Supporting Functions Start ----------------


# -------------- Supporting Functions End ----------------


# ------------------------------------------------------------------------------------------

@app.route('/getAllLogs', methods=['GET'])
def get_all_logs():
    db = client_monogo["patrakar_bhavan_db"]
    db1 = client_monogo["hall_booking_conf"]
    logs_collection = db1["logs"]
    members_db = db["members_db"]
    inquiry_db = db["inquiry_db"]
    bookings = db1["bookings"]
    canceledPaymentsPCH = db1["canceledPaymentsPCH"]
    # Get logs and exclude MongoDB's _id field
    logs = list(logs_collection.find({}, {"_id": 0}))

    # Get counts from collections
    total_members = members_db.count_documents({})
    total_inquiries = inquiry_db.count_documents({})
    all_bookings = bookings.count_documents({})
    canceled_bookings = canceledPaymentsPCH.count_documents({})

    # Get today's date in yyyy-MM-dd format
    today_date = datetime.today().strftime('%Y-%m-%d')
    todays_booking = bookings.count_documents({"date": today_date})

    return jsonify({
        "logs": logs[::-1], 
        "total_members": total_members,
        "total_inquiries": total_inquiries,
        "all_bookings": all_bookings,
        "todays_booking": todays_booking,
        "canceled_bookings": canceled_bookings
    })


# -------------------------------------------------------------------------------------------


if __name__ == '__main__':
    app.run()
