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

        
class ProdutoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Produto
        fields = '__all__'

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
        
class PedidoSerializer(serializers.ModelSerializer):
    itens = ItemPedidoSerializer(many=True)
    cliente_nome = serializers.CharField(
                        source='cliente.nome',
                        read_only=True
                    )
    total = serializers.SerializerMethodField()
    class Meta:
        model = Pedido
        fields = ['id', 'cliente', 'cliente_nome', 'status',
        'data_pedido', 'observacoes', 'itens', 'total']
        read_only_fields = ['data_pedido']
    def get_total(self, obj):
        return sum(i.quantidade * i.preco_unitario
                    for i in obj.itens.all())
    def create(self, validated_data):
        itens_data = validated_data.pop('itens')
        pedido = Pedido.objects.create(**validated_data)
        for item_data in itens_data:
            ItemPedido.objects.create(pedido=pedido, **item_data)
        return pedido
    
    def update(self, instance, validated_data):
        itens_data = validated_data.pop('itens', None)
        # Atualiza campos do pedido
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        # Substitui completamente os itens, se enviados
        if itens_data is not None:
            instance.itens.all().delete()
            for item_data in itens_data:
                ItemPedido.objects.create(pedido=instance, **item_data)
        return instance


