from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth import logout
from django.views.generic.base import TemplateView
from django.http import HttpResponse
from django.views import View


def calcular(v1, v2):
    return v1 / v2


#TODO: Refatorar para usar threads assim que possivel
def home(request):
    return render(request, 'home/home.html')


#FIXME: Corrigir bug ...
def my_logout(request):
    logout(request)
    return redirect('home')


class HomePageView(TemplateView):
    template_name = "home2.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['minha_variavel'] = 'Olá seja bem vindo ao curso de django avançado!'
        return context


class MyView(View):
    def get(self, request, *args, **kwargs):
        response = render_to_response("home/home3.html")
        #setando cookie
        response.set_cookie('color', 'blue', max_age=1000)
        return response

    def post(self, request, *args, **kwargs):
        return HttpResponse('Post')
