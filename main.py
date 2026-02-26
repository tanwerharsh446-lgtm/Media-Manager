from flask import Flask,render_template,request,redirect,url_for,session,flash,g
from database import data
import os
from werkzeug.security import generate_password_hash
from auth import verify_password,login_required,get_current_user,get_user_id,get_user_name,save_file,get_media

app = Flask(__name__)
app.secret_key = 'secret'

app.config['UPLOAD_FOLDER'] = 'user_uploads'

@app.before_request
def load_user():
    g.user = get_current_user()
    g.id = get_user_id()
    g.name = get_user_name()
  
@app.route("/")
def home():
    
    return render_template("index.html")

@app.route("/register",methods=["POST","GET"])
def register():
    return render_template("register.html")

@app.route("/get_register",methods=["POST"])
def get_register():
    get_d = data()
    name = request.form.get('name')
    email = request.form.get('email')
    password = generate_password_hash(request.form.get('password'))
    
    get_d.insert(name,email,password)
    return redirect(url_for('home'))


@app.route("/dashboard")
@login_required
def dashboard():
    obj = data()
    obj.create_table_notes()
    user=g.user
    id = obj.get_id(user)
    notes = obj.get_notes(user)
    
    
    dict_notes = {}
    if id and notes:
        for i,j in zip(id,notes):
        
            dict_notes[i[0]]=j[0]
    
    return render_template("dashboard.html",user=g.user,dict=dict_notes)
    
@app.route("/login",methods=["POST"])
def login():
    get_d = data()
    passw = request.form.get('password')
    email = request.form.get('email')

    if verify_password(passw,email):
        names = get_d.show_name(email)
        name = names[0]
        session['user_email'] = email
        session['user_name'] = name
        session['user_id'] = get_d.show_id(email)[0]


        return redirect(url_for('dashboard'))
    
    return "INVALID CREDITNTIOLS"

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route("/delete")
@login_required
def delete():
    d = data()
    d.delete(g.user)
    return redirect(url_for('home'))

@app.route("/add_note",methods=["POST"])
def add_note():
    obj = data()
    obj.insert_notes(g.user,request.form.get('note'))

    
    return redirect(url_for('dashboard'))    

@app.route("/delete_note/<int:node_id>")
def delete_note(node_id):
    obj = data()
    obj.delete_note(node_id,g.user)
    return redirect(url_for('dashboard'))

@app.route("/images")
def images():
    images = get_media('images',app.config["UPLOAD_FOLDER"],app.static_folder)

    return render_template('images.html',items=images,id=str(g.id))

@app.route("/videos")
def videos():
    videos = get_media('videos',app.config["UPLOAD_FOLDER"],app.static_folder)
    return render_template('videos.html',id=str(g.id),items=videos)

@app.route("/documents")
def documents():
    docs = get_media('documents',app.config["UPLOAD_FOLDER"],app.static_folder)
    return render_template('documents.html',id=str(g.id),items=docs)

@app.route('/get_images',methods=['POST'])
def get_images():
    save_file(app.static_folder,app.config['UPLOAD_FOLDER'],'images')
    return redirect(url_for('images'))
    

@app.route("/get_videos",methods=["POST"])
def get_videos():
    save_file(app.static_folder,app.config['UPLOAD_FOLDER'],'videos')
    return redirect(url_for('videos'))
    
    
@app.route("/get_documents",methods=["POST"])
def get_documents():
    save_file(app.static_folder,app.config['UPLOAD_FOLDER'],'documents')
    return redirect(url_for('documents'))
  
if __name__ == "__main__":
    app.run(debug=True)