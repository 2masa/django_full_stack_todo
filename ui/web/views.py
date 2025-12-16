import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from .services import APIClient

PRIORITY_OPTIONS = ["Highest", "High", "Medium", "Low"]
STATUS_OPTIONS = ["Open", "Pending", "InProgress", "Cancelled", "Completed"]

def login_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get("username")
            password = data.get("password")
        except json.JSONDecodeError:
            username = request.POST.get("username")
            password = request.POST.get("password")

        client = APIClient(request)
        response = client.login(username, password)

        if response and response.status_code == 200:
            request.session["auth_credential"] = response.json()
            return JsonResponse({
                "message": "Login successful!",
                "category": "success",
                "redirect_url": reverse('home')
            })
        else:
            msg = response.json().get("detail") if response else "Connection Error"
            return JsonResponse({"message": msg, "category": "error"}, status=401)

    return render(request, "login.html")

def home(request):
    if not request.session.get("auth_credential"):
        return redirect('login')
    return render(request, "home.html")

def get_todos(request):
    client = APIClient(request)
    response = client.get_todos()

    if response and response.status_code == 401:
        return redirect('login')
    
    todos = response.json() if response and response.status_code == 200 else []
    
    return render(request, "get_todos.html", {
        "data": todos,
        "priority_options": PRIORITY_OPTIONS,
        "status_options": STATUS_OPTIONS
    })

@require_http_methods(["POST"])
def add_todo(request):
    data = json.loads(request.body)
    client = APIClient(request)
    
    payload = {
        "title": data.get("title"),
        "priority": data.get("priority"),
        "status": data.get("status"),
        "description": data.get("description"),
    }
    
    response = client.add_todo(payload)
    if response.status_code == 200:
        return JsonResponse({
            "message": "Todo Added successfully.",
            "category": "success",
            "redirect_url": reverse('get_todos')
        })
    return JsonResponse({"message": "Failed to Add todo.", "category": "error"}, status=400)

@require_http_methods(["PATCH"])
def edit_todo(request, todo_id):
    data = json.loads(request.body)
    client = APIClient(request)
    
    payload = {
        "title": data.get("title"),
        "priority": data.get("priority"),
        "status": data.get("status"),
        "description": data.get("description"),
    }

    response = client.update_todo(todo_id, payload)
    if response.status_code == 200:
        return JsonResponse({
            "message": "Todo Updated successfully.",
            "category": "success",
            "redirect_url": reverse('get_todos')
        })
    return JsonResponse({"message": "Failed to Update todo.", "category": "error"}, status=400)

@require_http_methods(["DELETE"])
def delete_todo(request, todo_id):
    client = APIClient(request)
    response = client.delete_todo(todo_id)
    
    if response.status_code == 200:
        return JsonResponse({
            "message": "Todo Deleted successfully.",
            "category": "success",
            "redirect_url": reverse('get_todos')
        })
    return JsonResponse({"message": "Failed to Delete todo.", "category": "error"}, status=400)