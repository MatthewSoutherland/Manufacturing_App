from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session,
    url_for,
    flash,
)

from datetime import *
import csv
import secret

app = Flask(__name__)

# configure session
app.config["SECRET_KEY"] = secret.Secret_Key
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_COOKIE_SECURE"] = True
app.permanent_session_lifetime = timedelta(days=7)


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


@app.route("/truePos")
def truePos():
    return render_template("truePos.html")


@app.route("/feeds_speeds")
def feeds_speeds():
    return render_template("feeds_speeds.html")


@app.route("/toollist", methods=["GET", "POST"])
def toollist():
    if not session.get("name"):
        return redirect(url_for("login"))

    if request.method == "POST":
        return redirect(url_for("emailsent"))
    return render_template("toollist.html")


@app.route("/chips", methods=["GET", "POST"])
def chips():
    if not session.get("name"):
        return redirect(url_for("login"))

    hours = datetime.now().strftime("%H")
    hours = int(hours)
    day = datetime.today().strftime("%A")

    return render_template("chips.html", hours=hours, day=day)


@app.route("/emailsent")
def emailsent():

    return render_template("emailsent.html")


@app.route("/messagesent")
def messagesent():
    messageguy = request.args.get("messageguy")
    return render_template("messagesent.html", messageguy=messageguy)


@app.route("/trig_triangle")
def trig_triangle():
    if not session.get("name"):
        return redirect(url_for("login"))

    return render_template("trig_triangle.html")


if __name__ == "__main__":
    app.run(debug=True)
