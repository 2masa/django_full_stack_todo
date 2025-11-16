from functools import wraps
from flask import Flask, session, render_template,g

def auth_required(f):
    @wraps(f)
    def decorated_function(*args,**kwargs):
        user_data = session.get("user_data",{})
        token = user_data.get("access_token",None)

        if not user_data or not token:
            render_template("login.html")
        
        g.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }
        return f(*args,**kwargs)
    
    return decorated_function