"""This file contains the views for the login app."""

import json

from django.contrib.auth import authenticate
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def login_view(request: HttpRequest) -> JsonResponse:
    """Returns a JSON response with a message indicating if the login was successful or not."""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get("username")
            password = data.get("password")

            if not username or not password:
                return JsonResponse(
                    {"message": "Username and password are required"},
                    status=400,
                )

            user = authenticate(username=username, password=password)

            if user:
                return JsonResponse({"message": "Login successful"}, status=200)
            else:
                return JsonResponse(
                    {"message": "Username or password is not correct"},
                    status=401,
                )

        except json.JSONDecodeError:
            return JsonResponse({"message": "Invalid JSON format"}, status=400)

    return JsonResponse({"message": "Method not allowed"}, status=405)
