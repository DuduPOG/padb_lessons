from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Cliente, Endereco, Item, FormaPagamento, Vendedor, Pedido
from .serializers import ClienteSerializer, EnderecoSerializer, ItemSerializer, FormaPagamentoSerializer, VendedorSerializer, PedidoSerializer

class ClienteViewSet(viewsets.ModelViewSet):
    """
    ViewSet para o modelo Cliente.
    Fornece automaticamente os endpoints list, create, retrieve,
    update, partial_update e destroy.
    """
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    # Habilita filtros, busca textual e ordenação via query params
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['nome', 'email'] # ?nome=Maria
    search_fields = ['nome', 'email'] # ?search=Maria
    ordering_fields = ['nome', 'data_cadastro'] # ?ordering=-data_cadastro
    
class EnderecoViewSet(viewsets.ModelViewSet):
    
    queryset = Endereco.objects.all()
    serializer_class = EnderecoSerializer
    
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['rua', 'numero', 'bairro', 'cidade', 'estado', 'cep']
    search_fields = ['rua', 'numero', 'bairro', 'cidade', 'estado', 'cep']
    ordering_fields = ['cep']

class FormaPagamentoViewSet(viewsets.ModelViewSet):
    
    queryset = FormaPagamento.objects.all()
    serializer_class = FormaPagamentoSerializer
    
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['descricao']
    search_fields = ['descricao']
    ordering_fields = ['descricao']
    
class ItemViewSet(viewsets.ModelViewSet):        
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
        
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['nome', 'descricao', 'preco', 'estoque']
    search_fields = ['nome', 'preco']
    ordering_fields = ['nome']
        
    
class VendedorViewSet(viewsets.ModelViewSet):    
    queryset = Vendedor.objects.all()
    serializer_class = VendedorSerializer
    
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['nome', 'email', 'telefone']
    search_fields = ['nome', 'email']
    ordering_fields = ['nome']
    
class PedidoViewSet(viewsets.ModelViewSet):
    
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['data_pedido', 'data_entrega']
    search_fields = ['data_pedido', 'data_entrega']
    ordering_fields = ['data_pedido', 'data_entrega']