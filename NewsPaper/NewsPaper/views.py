from django.shortcuts import render


def index(request):  # HttpRequest
    return render(request, template_name='news/index.html')


# def get_login_redirect(request):
#     return render(request, template_name="protect/index.html")
