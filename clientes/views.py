from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.forms import model_to_dict
from .models import Person
from produtos.models import Produto
from vendas.models import Venda
from .forms import PersonForm
from django.views.generic import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.utils import timezone
from django.urls import reverse_lazy

@login_required
def persons_list(request):
    persons = Person.objects.all()
    return render(request, 'person.html', {'persons': persons})


@login_required
def persons_new(request):
    if not request.user.has_perm('clientes.add_person'):
        return HttpResponse('Não autorizado')
    form = PersonForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.save()
        return redirect('person_list')
    return render(request, 'person_form.html', {'form': form})


@login_required
def persons_update(request, id):
    1/0
    person = get_object_or_404(Person, pk=id)
    form = PersonForm(request.POST or None, request.FILES or None, instance=person)

    if form.is_valid():
        form.save()
        return redirect('person_list')

    return render(request, 'person_form.html', {'form': form})


@login_required
def persons_delete(request, id):
    person = get_object_or_404(Person, pk=id)

    if request.method == 'POST':
        person.delete()
        return redirect('person_list')

    return render(request, 'person_delete_confirm.html', {'person': person})


class PersonList(LoginRequiredMixin, ListView):
    model = Person

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        primeiro_acesso = self.request.session.get('primeiro_acesso', False)

        if not primeiro_acesso:
            context['message'] = 'Seja bem vindo ao seu primeiro acesso hoje'
            self.request.session['primeiro_acesso'] = True
        else:
            context['message'] = 'Você ja acessou hoje'
        return context


class PersonDetail(LoginRequiredMixin, DetailView):
    model = Person

    def get_object(self, queryset=None):
        pk = self.kwargs.get(self.pk_url_kwarg)
        return Person.objects.select_related('doc').get(id=pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        context['vendas'] = Venda.objects.filter(
            pessoa_id=self.object.id)
        return context


class PersonCreate(CreateView):
    model = Person
    fields = ['first_name', 'last_name', 'age', 'salary', 'bio', 'photo']

    def get_success_url(self):
        return reverse_lazy('person_list_cbv')


class PersonUpdate(UpdateView):
    model = Person
    fields = ['first_name', 'last_name', 'age', 'salary', 'bio', 'photo']
    success_url = reverse_lazy('person_list_cbv')


class PersonDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ('clientes.deletar_clientes',)
    model = Person

    def get_success_url(self):
        return reverse_lazy('person_list_cbv')

#inserir registros no banco de uma vez para ser mais rapido
class ProdutoBulk(View):
    def get(self, request):
        produtos = ['Banana', 'Maca', 'Limao', 'Laranja', 'Pera', 'Melancia']
        list_produtos = []

        for produto in produtos:
            p = Produto(descricao=produto, preco=10)
            list_produtos.append(p)

        Produto.objects.bulk_create(list_produtos)

        return HttpResponse('Funcionou')


def api(request):
    a = {'nome': 'Eric', 'idade': 25, 'salario':500}
    mensagem = {'mensagem': 'erro xzy'}
    lista = [1, 2, 3]

    produto = Produto.objects.last()

    b = model_to_dict(produto)

    produtos = Produto.objects.all()

    l = []

    for produto in produtos:
        l.append(model_to_dict(produto))

    return JsonResponse(l, status=200, safe=False)


class APICBV(View):
    def get(self, request):
        data = {'nome': 'Eric'}
        l = []

        produtos = Produto.objects.all()

        for produto in produtos:
            l.append(model_to_dict(produto))

        return JsonResponse(l, status=200, safe=False)


    def post(self, request):
        return JsonResponse('bom dia', status=200, safe=False)
