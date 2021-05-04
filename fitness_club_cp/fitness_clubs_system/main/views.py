from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    data = {
        'title': 'Главная страница',
        'values': ['Some', 'Hello', '123'],
        'obj' : {
            'car': 'BMV',
            'age': 18,
            'hobby': 'Football'
        }
    }
    return render(request, 'main/index.html', data)

def about(request):
    return render(request, 'main/about.html')