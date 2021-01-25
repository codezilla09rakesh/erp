from django.shortcuts import render

# Create your views here.

def Leave(req):
    return render(req, "leaves/leaves.html")
