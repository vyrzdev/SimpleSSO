from . import email
from sendgrid.helpers.mail import Mail


def sendVerificationEmail(usersEmail, verificationURL):
    message = Mail(
        from_email="verify@vyrz.dev",
        to_emails=usersEmail,
        html_content="Verify Email!"
    )
    message.dynamic_template_data = {
        "verification_url": verificationURL
    }
    message.template_id = "d-69e7733130974e958d044544b34d23eb"
    email.send(message)
