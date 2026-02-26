from flask import Flask,render_template,request,redirect,url_for,session,flash,g
from database import data
from functools import wraps
from werkzeug.security import generate_password_hash,check_password_hash
from werkzeug.utils import secure_filename
import os


def verify_password(passw,email):
    obj = data()
    
    user_pass = obj.show_password(email)
    if not user_pass:
        return False
    _pass = user_pass[0]
    return check_password_hash(_pass,passw)

def login_required(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        if 'user_id' not in session:
            return redirect(url_for('home'))
        return func(*args,**kwargs)
    return wrapper

def get_current_user():
    user = session.get('user_email')
    if user:
        return user
    return None

def get_user_id():
    user_id = session.get('user_id')
    if user_id:
        return user_id
    return None

def get_user_name():
    user_name = session.get('user_name')
    if user_name:
        return user_name
    return None

def save_file(static_folder,user_uploads,type):
    id = str(g.id)
    files = request.files
    if files:
        for key,file in request.files.items():
            
            filename = secure_filename(file.filename)
            if not file or filename=="":
                continue
            if (not(os.path.exists(os.path.join(static_folder,user_uploads,id,type)))):
                os.makedirs(os.path.join(static_folder,user_uploads,id,type),exist_ok=True)
            file.save(os.path.join(static_folder,user_uploads,id,type,filename))

def get_media(media_type,u_f,s_f):
    id = str(g.id)
    folder_path = os.path.join(s_f,u_f,id,media_type)
    if os.path.exists(folder_path):
        media = os.listdir(folder_path)
    else:
        media=[]

    return media

