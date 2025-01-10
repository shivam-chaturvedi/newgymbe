from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login
from .models import Users
from django.contrib.auth.hashers import make_password, check_password
import json

@csrf_exempt
def signup_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            email = data.get('email')
            password = data.get('password')

            if not name or not email or not password:
                return JsonResponse({'error': 'Name, email, and password are required'}, status=400)

            if Users.objects.filter(email=email).exists():
                return JsonResponse({'error': 'User already exists'}, status=400)

            hashed_password = make_password(password)
            user = Users.objects.create(name=name, email=email, password=hashed_password)
            return JsonResponse({'message': 'User created successfully'}, status=201)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')

            if not email or not password:
                return JsonResponse({'error': 'Email and password are required'}, status=400)

            try:
                user = Users.objects.get(email=email)

                if check_password(password, user.password):
                    return JsonResponse({'message': 'Login successful'}, status=200)
                else:
                    return JsonResponse({'error': 'Invalid credentials'}, status=401)

            except Users.DoesNotExist:
                return JsonResponse({'error': 'User does not exist'}, status=404)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
