from rest_framework import serializers
from .models import Cliente, Produto, Endereco, Item, FormaPagamento, Vendedor, Pedido


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__' # Inclui todos os campos do modelo
        # Para expor apenas alguns campos, use uma lista:
        # fields = ['id', 'nome', 'email']
        # Para excluir campos, use:
        # exclude = ['data_cadastro']
        
        
class EnderecoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endereco
        fields = '__all__'


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'
        
        
class FormaPagamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormaPagamento
        fields = '__all__'
        
        
class VendedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendedor
        fields = '__all__'
        
        
class ProdutoSerializer(serializers.ModelSerializer):
    categoria_display = serializers.CharField(
                            source='get_categoria_display',
                            read_only=True
                        )
    class Meta:
        model = Produto
        fields = '__all__' # inclui categoria_display automaticamente
        extra_fields = ['categoria_display']

        
class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = '__all__'
 