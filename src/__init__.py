from flask import Flask
from mongoengine import connect
from flask_login import LoginManager
from sendgrid import SendGridAPIClient


app = Flask(__name__, template_folder="html")
login = LoginManager(app)
email = SendGridAPIClient(
    api_key="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"
)

login.login_view = "login_identity"

from . import models

# Initialise DB.
connect(db="VyrzSSO")

from . import interfaces, utils, configurable, email_utils
from . import routes


def start(production: bool = None):
    app.secret_key = configurable.Configurables.Web.secret_key
    if production is None:
        print("Select Environment:")
        print("1 - Development")
        print("2 - Production")
        selection = None
        while selection not in ["1", "2"]:
            selection = input("- ")

        production = False
        if selection == "1":
            production = False
        elif selection == "2":
            production = True
        else:
            exit()

    if production:
        if configurable.Configurables.Web.secret_key == "DEFAULT-KEY-CHANGE-ME-BEFORE-PRODUCTION":
            print("You MUST change the secret key in src/configurables.py before production deployment!")
            print("Here is a randomly generated secret key for you to use:")
            print(f"{utils.generate_token()}-{utils.generate_token()}")
            exit()

        print("No production ready web server has been configured as of yet.")
        exit()
    else:
        email_utils.sendVerificationEmail("rattongaming@gmail.com", "https://www.google.com")
        app.run(host="0.0.0.0", port=5000, debug=True)
