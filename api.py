from flask import Flask, request, json
from flask_mail import Mail, Message
from decouple import config
from werkzeug.utils import secure_filename
import mimetypes
from validators.validator import Validators

app = Flask(__name__)

mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": config('EMAIL'),
    "MAIL_PASSWORD": config('PASSWORD'),
}

app.config.update(mail_settings)
mail = Mail(app)

validators = Validators()


@app.route("/send", methods=["POST"])
def send_mail():
    recipients = []
    count = 0
    while request.form.get('recipients'+str(count)) is not None:
        recipients.append(request.form.get('recipients'+str(count)))
        count += 1
    try:
        validators.validate_mail_recipients(recipients)

    except ValueError as e:
        print(e)
        resp = app.response_class(response=json.dumps({"error": str(e)}),
                                  status=500,
                                  mimetype="application/json")
        return resp

    msg = Message(subject="Hello",
                  sender=app.config.get("MAIL_USERNAME"),
                  recipients=recipients,
                  body="test email with attachment I sent with Gmail and Python Flask!")

    if 'email-attachments[]' in request.files:
        files = request.files.getlist('email-attachments[]')

        for file in files:
            filename = secure_filename(file.filename)

            ctype = mimetypes.MimeTypes().guess_type(filename)[0]

            if ctype is None:
                ctype = 'application/octet-stream'

            msg.attach(filename, ctype, file.read())

    mail.send(msg)

    return app.response_class(response={"status": "ok"},
                              status=200,
                              mimetype="application/json")


if __name__ == '__main__':
    app.run()


