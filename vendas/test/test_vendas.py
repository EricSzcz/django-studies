from django.test import TestCase
from vendas.models import Venda, ItemDoPedido
from produtos.models import Produto


class VendaTestCase(TestCase):
    def setUp(self):
        self.venda = Venda.objects.create(numero="123", desconto=10)
        self.produto = Produto.objects.create(descricao="produto 1", preco=10)

    def test_verifica_num_vendas_db(self):
        assert Venda.objects.all().count() == 1

    def test_valor_venda(self):
        """verifica valor total da venda"""
        ItemDoPedido.objects.create(
            venda=self.veda, produto=self.produto, quantidade=10)

        assert self.venda.valor == 90
