from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def home(request):
    #return HttpResponse("<h1>Hello, welcome to the home page</h1>")
    #return render(request, 'home.html')
    return render(request, 'home.html', {'name':'sebastian martinez'})
def about(request):
    return HttpResponse("<h1>welcome to the About page</h1>")