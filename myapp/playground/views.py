from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.shortcuts import get_object_or_404
import json
import os
from dotenv import load_dotenv
from .models import Blog

# Load envirnoment variables from .env file
load_dotenv()

@csrf_exempt
def index(request):
    if request.method == "POST":
        if not request.body:
            return JsonResponse({"message": "No information given"})
        
        body = json.loads(request.body)

        # Check if body contains blog title and content
        if "blogTitle" not in body or "blogContent" not in body:
            return JsonResponse({"message": "No blog information given"})
        
        b = Blog(title=body["blogTitle"], content=body["blogContent"], pub_date=timezone.now())
        b.save()

        latest_blogs = Blog.objects.order_by("-pub_date")[:5]
        latest_blogs_json = serializers.serialize("json", latest_blogs)
        
        return HttpResponse(latest_blogs_json, content_type="application/json")
    
    latest_blogs = Blog.objects.order_by("-pub_date")[:5]
    latest_blogs_json = serializers.serialize("json", latest_blogs)

    return HttpResponse(latest_blogs_json, content_type="application/json")

@csrf_exempt
def csrf(request):
    if not request.body:
        return JsonResponse({"message": "No information given"})

    print(request.body)
    body = json.loads(request.body)

    if "password" not in body:
        return JsonResponse({"message": "No password given"})
    
    if body["password"] != os.getenv("CSRF_PASSWORD"):
        return JsonResponse({"message": "Wrong password"})
    
    return JsonResponse({"csrfToken": get_token(request)})

@csrf_exempt
def comments(request, blog_id):
    if request.method == "POST":
        if not request.body:
            return JsonResponse({"message": "No information given"})
        
        body = json.loads(request.body)

        if "entryComment" not in body:
            return JsonResponse({"message": "No comment given"})
        
        blog = get_object_or_404(Blog, pk=blog_id)

        # Create comment for blog with given content
        blog.comment_set.create(content=body["entryComment"], pub_date=timezone.now())

        latest_comments = blog.comment_set.all().order_by("-pub_date")[:5]
        latest_comments_json = serializers.serialize("json", latest_comments)
        
        HttpResponse(latest_comments_json, content_type="application/json")

    blog = get_object_or_404(Blog, pk=blog_id)
    latest_comments = blog.comment_set.all().order_by("-pub_date")[:5]
    latest_comments_json = serializers.serialize("json", latest_comments)

    return HttpResponse(latest_comments_json, content_type="application/json")