import os
import subprocess
import re
from dotenv import load_dotenv


from flask import Flask, request, jsonify
from flask.views import MethodView
from marshmallow import Schema, fields, ValidationError


app = Flask(__name__)

load_dotenv()

API_KEY = os.getenv("API_KEY")
MAIL_HOSTNAME = os.getenv("MAIL_HOSTNAME")
HOSTNAME = MAIL_HOSTNAME.split(".", 1)[-1]
MIN_PASSWORD_LENGTH = int(os.getenv("MIN_PASSWORD_LENGTH", 6))


# decorator to check if the API key in request headers is valid
def check_api_key(f):
    def wrapper(*args, **kwargs):
        api_key = request.headers.get("Authorization")
        if api_key != API_KEY:
            return {"error": "Invalid API key"}, 401
        return f(*args, **kwargs)

    return wrapper


def validate_email(email):
    valid_email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if not re.match(valid_email_regex, email) and not email.endswith(f"@{HOSTNAME}"):
        raise ValidationError(
            f"Invalid email address. Must be a valid email and end with @{HOSTNAME}"
        )
    if has_dangerous_characters(email):
        raise ValidationError(
            "Email contains dangerous characters. Please use a different email."
        )
    return True


def validate_password(password):
    if len(password) < MIN_PASSWORD_LENGTH:
        raise ValidationError(
            f"Password must be at least {MIN_PASSWORD_LENGTH} characters long"
        )
    if has_dangerous_characters(password):
        raise ValidationError(
            "Password contains dangerous characters. Please use a different password."
        )
    return True


def run_command(command):
    # run command in the shell, and return True if successful, False otherwise
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"Command failed with error: {e.stderr.decode().strip()}")
        return False


def has_dangerous_characters(string):
    # Check for dangerous characters in the string
    dangerous_characters = [";", "&", "|", "`", "$", "\\", ">", "<"]
    return any(char in string for char in dangerous_characters)


class UserSchema(Schema):
    email = fields.Email(required=True, validate=validate_email)
    password = fields.Str(required=True, validate=validate_password)


class UserMails(MethodView):
    init_every_request = False
    decorators = [check_api_key]

    def post(self):
        request_data = request.get_json()

        if not request_data:
            return {"error": "Invalid request data"}, 400

        user_schema = UserSchema()
        errors = user_schema.validate(request_data)
        if errors:
            return {"error": errors}, 400

        email = request_data["email"]
        password = request_data["password"]

        cmd = f"setup email add {email} {password}"
        if not run_command(cmd):
            return {"error": "Failed to create mail"}, 500

        return jsonify({"message": "Mail created successfully"}), 201

    def patch(self):
        request_data = request.get_json()

        if not request_data:
            return {"error": "Invalid request data"}, 400

        user_schema = UserSchema()
        errors = user_schema.validate(request_data)
        if errors:
            return {"error": errors}, 400

        email = request_data["email"]
        password = request_data["password"]

        cmd = f"setup email update {email} {password}"
        if not run_command(cmd):
            return {"error": "Failed to update mail"}, 500

        return jsonify({"message": "Mail updated successfully"}), 200

    def delete(self):
        request_data = request.get_json()

        if not request_data:
            return {"error": "Invalid request data"}, 400

        email = request_data.get("email")
        if not email:
            return {"error": "Invalid email"}, 400

        if not validate_email(email):
            return {"error": "Invalid email"}, 400

        if has_dangerous_characters(email):
            return {"error": "Email contains dangerous characters"}, 400

        cmd = f"setup email del {email}"

        if not run_command(cmd):
            return {"error": "Failed to delete mail"}, 500

        return jsonify({"message": "Mail deleted successfully"}), 200


app.add_url_rule(
    "/user_mails",
    view_func=UserMails.as_view("user_mails"),
    methods=["POST", "PATCH", "DELETE"],
)
