from rest_framework import serializers
from .models import Cliente, Produto, Endereco, Item, FormaPagamento, Vendedor, PerfilVendedor, Pedido, ItemPedido


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
        
"""
class PerfilVendedorSerializer(serializers.ModelSerializer):
    vendedor_nome = serializers.CharField(
                        source='vendedor.nome',
                        read_only=True
                    )
    class Meta:
        model = PerfilVendedor
        fields = ['vendedor', 'vendedor_nome', 'razao_social',
        'inscricao_estadual', 'banco', 'agencia',
        'conta', 'chave_pix']
"""
        
class ProdutoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Produto
        fields = '__all__'

        
class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = '__all__'
"""
class ItemPedidoSerializer(serializers.ModelSerializer):
    produto_nome = serializers.CharField(
                    source='produto.nome',
                   read_only=True
                )
    subtotal = serializers.SerializerMethodField()


    class Meta:
        model = ItemPedido
        fields = ['id', 'produto', 'produto_nome',
        'quantidade', 'preco_unitario', 'subtotal']
        
        def get_subtotal(self, obj):
            return obj.quantidade * obj.preco_unitario
"""
