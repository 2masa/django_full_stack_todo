import requests
import sys
from django.conf import settings

class APIClient:
    def __init__(self, request):
        self.base_url = settings.FASTAPI_BASE_URL
        self.session = request.session
        self.token = self.session.get('auth_credential', {}).get('access_token')

    @property
    def headers(self):
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def login(self, username, password):
        payload = {"username": username, "password": password}
        try:
            # Debugging print to help verify connections
            print(f"DEBUG: Connecting to {self.base_url}/auth/login")
            response = requests.post(f"{self.base_url}/auth/login", data=payload, timeout=5)
            return response
        except requests.RequestException as e:
            print(f"API ERROR: {e}")
            sys.stdout.flush()
            return None

    def get_todos(self):
        try:
            return requests.get(f"{self.base_url}/todo/", headers=self.headers, timeout=5)
        except requests.RequestException:
            return None

    def add_todo(self, data):
        return requests.post(f"{self.base_url}/todo/", json=data, headers=self.headers)

    def update_todo(self, todo_id, data):
        data['id'] = str(todo_id)
        return requests.patch(f"{self.base_url}/todo/", json=data, headers=self.headers)

    def delete_todo(self, todo_id):
        return requests.delete(f"{self.base_url}/todo/", json=[str(todo_id)], headers=self.headers)