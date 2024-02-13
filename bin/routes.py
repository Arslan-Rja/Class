from app import app
import users
from flask import Flask, render_template, request, redirect, url_for, session


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/classes")
        else:
            return render_template("error.html")
            
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        userType = request.form["userType"]
        teachercode = request.form["teachercode"]
        if users.register(username, password, userType, teachercode):
            return redirect("/classes")
        else:
            return render_template("errorTeachercode.html")

@app.route("/")
def index():
	return render_template('index.html')

@app.route("/classes", methods=["GET", "POST"])
def classes():
    if request.method == "GET":
        classes_list = users.get_classes()
        return render_template("classes.html", classes=classes_list)
    elif request.method == "POST":
        class_name = request.form["class_name"]
        users.add_class(class_name)
        return redirect(url_for("classes"))


@app.route("/join_class/<int:class_id>")
def join_class(class_id):
    class_info = users.get_class_info(class_id)
    return redirect(url_for("chat", class_id=class_id))

@app.route("/delete_class/<int:class_id>", methods=["POST"])
def delete_class(class_id):
    result = users.delete_class(class_id)
    return redirect(url_for("classes"))


@app.route("/send_message/<int:class_id>", methods=["POST"])
def send_message(class_id):
    content = request.form.get("content")
    user_id = session.get("user_id")
    users.send_message(user_id, class_id, content)
    return redirect(url_for("chat", class_id=class_id))
    
@app.route("/edit_message/<int:message_id>/<int:class_id>", methods=["POST"])
def edit_message(message_id, class_id):
    editted = request.form.get("editted")
    users.edit_message(message_id, editted)
    return redirect(url_for("chat", class_id=class_id))

@app.route("/delete_message/<int:message_id>/<int:class_id>", methods=["POST"])
def delete_message(message_id, class_id):
    user_id = session.get("user_id")
    result = users.delete_message(message_id, user_id)
    return redirect(url_for("chat", class_id=class_id))

@app.route("/chat/<int:class_id>")
def chat(class_id):
    messages = users.get_messages(class_id)
    return render_template("chat.html", class_id=class_id, messages=messages)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

