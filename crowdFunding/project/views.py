from django.shortcuts import render

def hello(request):
    print(request)
    return render(request, 'test.html', {'name': 'Hello'})
