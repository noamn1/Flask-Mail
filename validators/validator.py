from validate_email import validate_email


class Validators:

    def validate_mail_recipients(self, recipients):
        if not recipients or len(recipients) == 0:
            raise ValueError("No recipients provided:")

        for recipient in recipients:
            is_valid = validate_email(recipient)
            if not is_valid:
                raise ValueError("Invalid email: " + recipient)
