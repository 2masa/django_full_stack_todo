from flask import Flask, flash, jsonify, redirect, render_template, request, session, g, url_for
from flask_session.redis import RedisSessionInterface
import requests

from config import settings
from redis_client import RedisClient
from models import priority_options, status_options

app = Flask(__name__, template_folder="templates", static_folder="static")
app.session_interface = RedisSessionInterface(app=app, client=RedisClient)
app.secret_key = settings.flask_security_key


FASTAPI_BASE_URL = settings.fastapi_base_url


@app.before_request
def set_common_headers():
    # This runs before every request to the app
    if request.path.startswith("/static/") or request.path == url_for("login"):
        return

    user_data: dict = session.get("auth_credential", {})

    if not user_data:
        return redirect(url_for("login"))
    token = user_data.get("access_token")

    if not token:
        # Token is missing from user data, redirect to login
        return redirect(url_for("login"))

    # Store the headers in the g object
    g.api_headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }


@app.route("/", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        data = request.get_json()
        payload = {"username": data.get("username"), "password": data.get("password")}
        response = requests.post(url=f"{FASTAPI_BASE_URL}/auth/login", data=payload)
        if response.status_code == 200:
            session["auth_credential"] = response.json()
            return jsonify({"message":"Login successful!","category":"success","redirect_url":"/home"})
        else:
            msg = response.json().get("detail")
            return jsonify({"message":msg,"category":"error"})

    return render_template("login.html")


@app.route("/home")
def home():
    """Renders the ain index page."""
    response = requests.get(f"{FASTAPI_BASE_URL}/todo/", headers=g.api_headers)
    if response.status_code == 401:
        return redirect(url_for("login"))
    return render_template("home.html")


@app.route("/todos", methods=["GET"])
def get_todos():
    response = requests.get(f"{FASTAPI_BASE_URL}/todo/", headers=g.api_headers)
    if response.status_code == 200:
        data = response.json()
        return render_template(
            "get_todos.html",
            data=data,
            priority_options=priority_options,
            status_options=status_options,
        )
    elif response.status_code == 401:
        return redirect(url_for("login"))
    else:
        msg = response.json().get("detail")
        return render_template("flash_message.html", msg=msg, time=1000)


@app.route("/todo/add", methods=["POST"])
def add_todo():
    data = request.get_json()
    payload = {
        "title": data.get("title"),
        "priority": data.get("priority"),
        "status": data.get("status"),
        "description": data.get("description"),
    }
    response = requests.post(
        f"{FASTAPI_BASE_URL}/todo/", json=payload, headers=g.api_headers
    )

    if response.status_code == 200:
        return jsonify({"message": "Todo Added successfully.","category":"success","redirect_url":"/todos"})
    else:
        return jsonify({"message": "Failed to Add todo.","category":"error"})



@app.route("/todo/edit/<uuid:todo_id>", methods=["PATCH"])
def edit_todo(todo_id):
    data = request.get_json()
    payload = {
        "id": str(todo_id),
        "title": data.get("title"),
        "priority": data.get("priority"),
        "status": data.get("status"),
        "description": data.get("description"),
    }

    response = requests.patch(
        f"{FASTAPI_BASE_URL}/todo/", json=payload, headers=g.api_headers
    )
    if response.status_code == 200:
        msg = (
            "Successfully Completed todo!."
            if data.get("status") == "Completed"
            else "Todo Updated successfully."
        )
        return jsonify({"message":msg,"category":"success","redirect_url":"/todos"})
    else:
        return jsonify({"message":"Failed to Update todo.","category":"error"})



@app.route("/todo/delete/<uuid:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    response = requests.delete(
        f"{FASTAPI_BASE_URL}/todo/", json=[str(todo_id)], headers=g.api_headers
    )

    if response.status_code == 200:
        return jsonify({"message": "Todo Deleted successfully.","category":"success","redirect_url":"/todos"})            
    else:
        return jsonify({"message":"Failed to Delete todo.","category":"error"})


if __name__ == "__main__":
    app.run(
        debug=settings.flask_debug,
        port=settings.flask_port,
        host=settings.flask_host
    )
