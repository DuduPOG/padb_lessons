from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Cliente, Produto, Item, Vendedor, PerfilVendedor, Pedido, ItemPedido
from .serializers import ClienteSerializer, ProdutoSerializer, ItemSerializer, VendedorSerializer, PerfilVendedorSerializer, PedidoSerializer, ItemPedidoSerializer

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
    
class PerfilVendedorViewSet(viewsets.ModelViewSet):
    queryset = PerfilVendedor.objects.select_related('vendedor').all()
    serializer_class = PerfilVendedorSerializer
    
class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
    
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['nome', 'descricao', 'preco', 'data_cadastro']
    search_fields = ['nome', 'descricao', 'preco', 'data_cadastro',]
    ordering_fields = ['nome']
    
class PedidoViewSet(viewsets.ModelViewSet):
    serializer_class = PedidoSerializer
    def get_queryset(self):
        return (Pedido.objects
                .select_related('cliente')
                .prefetch_related('itens__produto')
                .all())
        
class ItemPedidoViewSet(viewsets.ModelViewSet):
    queryset = ItemPedido.objects.select_related('pedido', 'produto').all()
    serializer_class = ItemPedidoSerializer
