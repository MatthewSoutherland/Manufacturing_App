from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session,
    url_for,
    flash,
    sessions,
)

from flask_mail import Message, Mail
from datetime import *
import csv
import json
import vonage

app = Flask(__name__)

# configure session
app.config[
    "SECRET_KEY"
] = "192f9bdd21ab9ed4d82e236c78afcb3a393ec15f71bbr5dc987d54727823bcbd"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_COOKIE_SECURE"] = True
app.permanent_session_lifetime = timedelta(days=1)

# SMS message setup
client = vonage.Client(key="a0d95cf9", secret="U0Eg3thF3kUBNkal")
sms = vonage.Sms(client)

# initialize mail for this app

app.config["MAIL_SERVER"] = "mail.merrilltg.com"
# app.config['MAIL_PORT'] = 465
app.config["MAIL_USERNAME"] = "compliance@merrilltg.com"
app.config["MAIL_PASSWORD"] = "cllvhzgljixztfnh"
app.config["MAIL_DEFAULT_SENDER"] = "compliance@merrilltg.com"
app.config["MAIL_MAX_EMAILS"] = 2
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True

mail = Mail(app)
# mail.init_app(app)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Create global functions to read centerlines
def read_mz4a_center_lines():
    with open("mz4a.csv", "r") as f:
        reader = csv.reader(f)
        for row in reader:
            mz4a_cl = row
    return mz4a_cl


def read_mz4b_center_lines():
    with open("mz4b.csv", "r") as f:
        reader = csv.reader(f)
        for row in reader:
            mz4b_cl = row
    return mz4b_cl


def read_mz4c_center_lines():
    with open("mz4c.csv", "r") as f:
        reader = csv.reader(f)
        for row in reader:
            mz4c_cl = row
    return mz4c_cl


@app.route("/")
def home():
    if not session.get("name"):
        return redirect(url_for("login"))
    return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        password = request.form.get("password")
        user_name = request.form.get("username")

        if not user_name:
            flash("Please enter user name")
            return render_template("login.html")
        if password == "wb04":
            session["name"] = user_name
            return redirect(url_for("home"))
        else:
            flash("Incorrect password")

    return render_template("login.html")


@app.route("/logout")
def logout():

    # Forget any user_id

    session.clear()

    # Redirect user to login form
    return redirect(url_for("login"))


@app.route("/taps_drills", methods=["GET", "POST"])
def taps_drills():
    if not session.get("name"):
        return redirect(url_for("login"))
    return render_template("taps_drills.html")


@app.route("/ports", methods=["GET", "POST"])
def ports():
    if not session.get("name"):
        return redirect(url_for("login"))

    return render_template("ports.html")


@app.route("/mz4", methods=["GET", "POST"])
def mz4():
    if not session.get("name"):
        return redirect(url_for("login"))
    mz4a = read_mz4a_center_lines()
    mz4b = read_mz4b_center_lines()
    mz4c = read_mz4c_center_lines()

    return render_template("mz4.html", mz4a=mz4a, mz4b=mz4b, mz4c=mz4c)


@app.route("/mz4cl", methods=["GET", "POST"])
def mz4cl():
    if not session.get("name"):
        return redirect(url_for("login"))
    mz4a = read_mz4a_center_lines()
    mz4b = read_mz4b_center_lines()
    mz4c = read_mz4c_center_lines()

    if request.method == "POST":
        if request.form.get("mz4ax"):
            with open("mz4a.csv", "w", newline="") as f:
                writer = csv.writer(f, delimiter=",")
                new = request.form.get("mz4ax")
                new1 = request.form.get("mz4az")
                new2 = [new, new1]
                writer.writerow(new2)
        elif request.form.get("mz4bx"):
            with open("mz4b.csv", "w", newline="") as f:
                writer = csv.writer(f, delimiter=",")
                new = request.form.get("mz4bx")
                new1 = request.form.get("mz4bz")
                new2 = [new, new1]
                writer.writerow(new2)
        elif request.form.get("mz4cx"):
            with open("mz4c.csv", "w", newline="") as f:
                writer = csv.writer(f, delimiter=",")
                new = request.form.get("mz4cx")
                new1 = request.form.get("mz4cz")
                new2 = [new, new1]
                writer.writerow(new2)
        return redirect(url_for("mz4"))

    return render_template("mz4cl.html", mz4a=mz4a, mz4b=mz4b, mz4c=mz4c)


@app.route("/toollist", methods=["GET", "POST"])
def toollist():

    if not session.get("name"):
        return redirect(url_for("login"))
    if request.method == "POST":

        exInput = request.form["exInput"]
        msg = Message("Tool List", recipients=["ToolList@outlook.com"])
        msg.html = json.loads(exInput)
        mail.send(msg)
        return redirect(url_for("emailsent"))
    return render_template("toollist.html")


@app.route("/chips", methods=["GET", "POST"])
def chips():
    if not session.get("name"):
        return redirect(url_for("login"))

    # the hours run in developent will be local time.
    # The app is run off a london server so in production,
    # the template conditionals will be different.
    hours = datetime.today().now().strftime("%H")
    hours = int(hours)
    day = datetime.today().strftime("%A")

    if request.method == "POST":
        message1 = request.form.get("message1")
        responseData = sms.send_message(
            {"from": "18777738885", "to": "19895992017", "text": message1}
        )
        if responseData["messages"][0]["status"] == "0":
            messageguy = "message sent successfully"
            return redirect(url_for("messagesent", messageguy=messageguy))
        else:
            messageguy = f"Message failed with error: {responseData['messages'][0]['error-text']}"
            return redirect(url_for("messagesent", messageguy=messageguy))

    return render_template("chips.html", hours=hours, day=day)


@app.route("/emailsent")
def emailsent():

    return render_template("emailsent.html")


@app.route("/messagesent")
def messagesent():
    messageguy = request.args.get("messageguy")
    return render_template("messagesent.html", messageguy=messageguy)


@app.route("/calculator")
def calculator():
    if not session.get("name"):
        return redirect(url_for("login"))

    return render_template("calculator.html")


# comment out in production
if __name__ == "__main__":
    app.run(debug=True)
