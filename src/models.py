import mongoengine
import cerberus
from werkzeug.security import generate_password_hash, check_password_hash
from .utils import generate_token
from .configurable import Configurables
from flask_login import UserMixin, current_user
from datetime import datetime
from . import login

_own_authorised_app_instance = None


def own_authorised_app():
    """
    An epic proxy function that will return and cache the AuthorisedApp instance of this whole app!

    :return: AuthorisedApp
    """
    global _own_authorised_app_instance
    if _own_authorised_app_instance is None:
        authorisedApp: AuthorizedApplication = AuthorizedApplication.objects(
            application_name="root"
        ).first()
        if authorisedApp is None:
            authorisedApp = AuthorizedApplication(
                application_name="root",
                developer_email="ben@vyrz.dev"
            )
            authorisedApp.save()

        _own_authorised_app_instance = authorisedApp
        return authorisedApp
    else:
        return _own_authorised_app_instance


def get_identity_object():
    return Identity.objects(id=current_user.id).first()


@login.user_loader
def identity_loader(identity_id):
    return Identity.objects(id=identity_id).first()


class Identity(mongoengine.Document, UserMixin):
    """
    Representation of a user.
    """
    email = mongoengine.EmailField(required=True)
    password_hash = mongoengine.StringField()

    def setPassword(self, password_text):
        self.password_hash = generate_password_hash(password_text)

    def checkPassword(self, password_text):
        return check_password_hash(self.password_hash, password_text)

    def api_dump(self):
        return {
            "id": str(self.id),
            "email": str(self.email)
        }


class AuthorizedApplication(mongoengine.Document):
    application_name = mongoengine.StringField(required=True)
    developer_email = mongoengine.EmailField(required=True)
    application_secret = mongoengine.StringField(default=generate_token)


class IdentityAuthorizationSession(mongoengine.Document):
    identity: Identity = mongoengine.ReferenceField(Identity, required=True)
    application: AuthorizedApplication = mongoengine.ReferenceField(AuthorizedApplication, required=True)
    expiresAt: datetime = mongoengine.DateTimeField(required=True)
    token: str = mongoengine.StringField
