from . import app, models, utils, interfaces
from flask import request, redirect, render_template, jsonify
from furl import furl
from flask_login import login_required, current_user, login_user, logout_user


def createLoginSession(identity) -> models.IdentityAuthorizationSession:
    newIdentityAuthorizationSession = models.IdentityAuthorizationSession(
        identity=identity,
        expiresAt=utils.future(minutes=20)
    )
    newIdentityAuthorizationSession.save()
    return newIdentityAuthorizationSession


def redirectSession(redirectURL: str, identityAuthSession: models.IdentityAuthorizationSession):
    return redirect(furl(redirectURL).add({"token": identityAuthSession.token}).url)


@app.route("/")
@login_required
def home():
    return "Homepage"


@app.route("/login", methods=["GET", "POST"])
def login_identity():
    redirectURL = request.args.get("redirectURL")
    if redirectURL is None:
        redirectURL = ""
    if current_user.is_authenticated:
        identitySession = createLoginSession(models.get_identity_object())
        if redirectURL not in ["", None]:
            return redirectSession(redirectURL, identitySession)
        else:
            return redirect("/")
    else:
        if request.method == "GET":
            return render_template("form-pages/login.html", title="Login with VyrzSSO", redirectURL=redirectURL)
        else:
            email = request.form.get("email")
            password = request.form.get("password")
            if email in ["", None]:
                return render_template("form-pages/login.html", title="Login with VyrzSSO", redirectURL=redirectURL, alerts=[interfaces.Alert("Email Required!")])
            if password in ["", None]:
                return render_template("form-pages/login.html", title="Login with VyrzSSO", redirectURL=redirectURL, alerts=[interfaces.Alert("Password Required!")])

            identity = models.Identity.objects(
                email=email
            ).first()
            if (identity is None) or (not identity.checkPassword(password)):
                return render_template("form-pages/login.html", title="Login with VyrzSSO", redirectURL=redirectURL, alerts=[interfaces.Alert("Invalid Email or Password!")])

            login_user(identity)
            identitySession = createLoginSession(identity)
            if redirectURL not in ["", None]:
                return redirectSession(redirectURL, identitySession)
            else:
                return redirect("/")


@app.route("/register", methods=["POST", "GET"])
def register_identity():
    redirectURL = request.args.get("redirectURL")
    if redirectURL is None:
        redirectURL = ""
    if current_user.is_authenticated:
        identitySession = createLoginSession(models.get_identity_object())
        if redirectURL not in ["", None]:
            return redirectSession(redirectURL, identitySession)
        else:
            return redirect("/")
    else:
        if request.method == "GET":
            return render_template("form-pages/register.html", title="Register for VyrzSSO", redirectURL=redirectURL)
        else:
            email = request.form.get("email")
            password, confirm_password = request.form.get("password"), request.form.get("confirm_password")
            if email in ["", None]:
                return render_template("form-pages/register.html", title="Register for VyrzSSO", redirectURL=redirectURL, alerts=[interfaces.Alert("Email Required!")])
            if password in ["", None]:
                return render_template("form-pages/register.html", title="Register for VyrzSSO", redirectURL=redirectURL, alerts=[interfaces.Alert("Password Required!")])
            if confirm_password != password:
                return render_template("form-pages/register.html", title="Register for VyrzSSO", redirectURL=redirectURL, alerts=[interfaces.Alert("Passwords Do Not Match!")])

            # Create a new identity here for now!
            newIdentity = models.Identity(
                email=email,
            )
            newIdentity.setPassword(password)
            newIdentity.save()
            login_user(newIdentity)

            newIdentityAuthorizationSession = createLoginSession(newIdentity)
            if redirectURL not in ["", None]:
                return redirectSession(redirectURL, newIdentityAuthorizationSession)
            else:
                return redirect("/")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/api/v1")
def info():
    return """
        A scuffed identity API...    
    """


@app.route("/api/v1/get_identity")
def get_identity():
    authSessionToken = request.args.get("token")
    if authSessionToken is None or authSessionToken == "":
        return jsonify({
            "message": "Missing Auth Token..."
        }), 500

    authSessionObject: models.IdentityAuthorizationSession = models.IdentityAuthorizationSession.objects(
        token=authSessionToken
    ).first()
    if (authSessionObject is None) or (authSessionObject.expiresAt < utils.future()):
        return {
            "message": "Invalid Auth Token..."
        }, 400

    usersIdentity = authSessionObject.identity

    return jsonify(usersIdentity.api_dump())
