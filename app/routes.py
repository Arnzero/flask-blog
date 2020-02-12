#import certain functions into the global
#namespace
from app import app
from markdown import markdown
from flask import render_template, render_template_string, request, session, url_for, redirect, flash
from app.blog_helpers import render_markdown
from os import walk
import os

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
    error =""
    if request.method == 'POST':
        if request.form['user_name'] !='admin' or request.form['password'] != 'password':
            error ='INVALID CREDENTAIALS'
        else:
            session['logged_in'] = True
            return redirect(url_for('edit', 'about'))
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



@app.route("/edit/<page_name>")
def edit(page_name):
    view_data = {}
    view_data["pages"] = []

    data = {}
    

    for(dirpath, dirnames, filenames) in walk(r'C:\Users\arnze\Desktop\flask-blog\app\templates'):
        for file in filenames:
         view_data["pages"].append(file.rsplit(".",1)[0])
         data[file.rsplit(".",1)[0]] = file
    html = ""
    #data[pages] = render_markdown(page_name + ".md" )
    path = os.path.join(r'C:\Users\arnze\Desktop\flask-blog\app\templates', data[page_name])
    with open(path) as html_file:
        html = html_file.read()
    #html = render_markdown(page)
        
    
    return render_template("edit.html", page_name=render_template_string(html))