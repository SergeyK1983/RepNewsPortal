from django.shortcuts import render


def index(request):  # HttpRequest
    return render(request, template_name='index.html')
