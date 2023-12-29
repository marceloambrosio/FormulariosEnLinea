from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View

# Create your views here.
class HomeView(View):
    def get(self, request):
        return render(request, 'home.html')