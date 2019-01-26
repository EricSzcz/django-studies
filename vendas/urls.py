from django.urls import path
from .views import DashboardView, NovoPedido, NovoItemPedido,\
                   ListaVendas, EditPedido, ExcluiItemPedido, ExcluirPedido, EditItemPedido


urlpatterns = [
    path('', ListaVendas.as_view(), name="lista-vendas"),
    path('novo-pedido/', NovoPedido.as_view(), name="novo-pedido"),
    path('novo-item-pedido/<int:venda>/', NovoItemPedido.as_view(), name="novo-item-pedido"),
    path('edit-pedido/<int:venda>/', EditPedido.as_view(), name="edit-pedido"),
    path('excluir-pedido/<int:venda>/', ExcluirPedido.as_view(), name="excluir-pedido"),
    path('edit-item-pedido/<int:item>/', EditItemPedido.as_view(), name="edit-item-pedido"),
    path('exclui-item-pedido/<int:item>/', ExcluiItemPedido.as_view(), name="exclui-item-pedido"),
    path('dashboard/', DashboardView.as_view(), name="dashboard"),
]
