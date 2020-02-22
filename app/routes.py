#import certain functions into the global
#namespace
from app import app
from markdown import markdown
from flask import render_template, render_template_string, request, session, url_for, redirect, flash
from app.blog_helpers import render_markdown
from os import walk
import os
#from users import user
#from app.python-sqlite
import sqlite3
#from users import Users

import codecs



app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.run(debug=True, host= '0.0.0.0')

#safe global import (okay to use)
import flask

#global import (try to avoid)
#from flask import *

#home page
@app.route("/")
def home():
    return render_markdown('index.md')

@app.route("/veganCelebrities")
def veganCelebrities():
    return render_template("veganCelebrities.html")


@app.route("/formTest")
def formTest():
    return render_template("formTest.html")

@app.route('/all')
def all():
    view_data = {}
    view_data["pages"] = []

    data = {}
    

    for(dirpath, dirnames, filenames) in walk(r'C:\Users\arnze\Desktop\flask-blog\app\templates'):
        for file in filenames:
         view_data["pages"].append(file.rsplit(".",1)[0])
         data[file.rsplit(".",1)[0]] = file
    return render_template("all.html", data=view_data)

@app.route('/login', methods=['GET', 'POST'])
def login():
    conn = sqlite3.connect('users.db')

    c = conn.cursor()

    def insert_user(usr):
        with conn:
            c.execute("INSERT INTO pyUsers VALUES (:UserLogin, :PW)", {'UserLogin':usr.UserLogin, 'PW':usr.PW})


    def get_userName():
        with conn:
            c.execute("SELECT pyUserName FROM pyUsers")
        return c.fetchone()

    def get_PassW():
        with conn:
            c.execute("SELECT pyPassword FROM pyUsers")
        return c.fetchone()
   
    
    error =""
    un = get_userName()
    pww = get_PassW()
    conn.close()
    if un[0] == 'admin':
        print("match")
    
    print(un[0])
    



    if request.method == 'POST':
        if request.form['user_name'] != un[0] or request.form['password'] != pww[0]:
            error ="invalid credentials!"
        else:
            session['logged_in'] = True
            return redirect(url_for('home'))
    return render_template("login.html", error=error)

@app.route("/favicon.ico")
def favicon():
    return ""

@app.route("/click_tracker", methods=['GET', 'POST'])
def click_tracker():
    view_data = {}
    view_data["click_count"] = 0
    if request.method == 'POST':
        view_data["click_count"] = request.values["click_count"]
        view_data["click_count"] = int(view_data["click_count"]) + 1
    return render_template('click_tracker.html', data=view_data)
    

#generic page
@app.route("/<view_name>")

#input parameter name must match route parameter
def render_page(view_name):
    html = render_markdown(view_name + '.md')
    view_data = {} #create empty dictionary
    return render_template_string(html, view_data = session)

@app.route("/edit/", methods = ['GET','POST'])
def edit():
    view_data = {}
    view_data['page_name'] = ""
    view_data['content'] = "content etc."
    dir_path = 'app/templates'
    edit_page = 'edit.html'
    

    return render_template(edit_page, data=view_data)

@app.route("/edit/<view_name>", methods=['GET', 'POST'])
def edit_page(view_name):

    # Acknowledge all the files in directory
    fileAlias = {}
    for(dirpath, dirnames, filenames) in walk(r'C:\Users\arnze\Desktop\flask-blog\app\templates'):
        for file in filenames:
            fileAlias[file.rsplit(".",1)[0]] = file

    # Acknowledge the page to be edit
    view_data = {}
    #view_name = view_name.rsplit(".",1)[0]
    view_data['page_name'] = view_name
    view_edit = 'edit.html'
    
    dir_path = 'app/templates'

    # Form an absolute address to project files
    path = os.path.join(dir_path, fileAlias[view_name])


    tempfile = open(path, "r")
    contents = tempfile.read()
    wrd = ""
    ff = codecs.open( path, "r", "utf-8")
    wrd = ff.read()
    view_data["content"] = render_template_string(fileAlias[view_name])
    tempfile.close()

    # If we came from POST, write to file from 'form'
    if request.method == 'POST':
        f = open(path, "w")
        updated_content = request.values["content"]
        print (updated_content)
        f.write(str(updated_content))
        f.close()
        path = os.path.join(dir_path, fileAlias[request.values['page_name']] )
    
        # Read content from form
        #view_data["content"] = request.values["content"]


    return render_template(view_edit, data=view_data)

   

   

    
  

    


