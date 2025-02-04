from django.http import HttpResponse
from django.shortcuts import redirect
def docs(request):
    return redirect('redoc/')
