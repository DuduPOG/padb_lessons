from django.contrib import admin
from .models import Cliente, Endereco, FormaPagamento, Item, Produto, Vendedor, PerfilVendedor, Pedido, ItemPedido

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'telefone', 'data_cadastro')
    search_fields = ('nome', 'email')
    ordering = ('nome',)

@admin.register(Endereco)
class EnderecoAdmin(admin.ModelAdmin):
    list_display = ('rua', 'numero', 'bairro', 'cidade', 'estado', 'cep')
    search_fields = ('rua', 'numero', 'bairro', 'cidade', 'estado', 'cep')
    ordering = ('cep',)
    
@admin.register(FormaPagamento)
class FormaPagamentoAdmin(admin.ModelAdmin):
    list_display = ('descricao',)
    search_fields = ('descricao',)
    ordering = ('descricao',)
    
@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao', 'preco', 'estoque')
    search_fields = ('nome', 'preco')
    ordering = ('nome',)
    
@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao', 'preco', 'data_cadastro')
    search_fields = ('nome', 'descricao', 'preco', 'data_cadastro')
    ordering = ('nome', 'preco', 'data_cadastro')
    
@admin.register(Vendedor)
class VendedorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'telefone')
    search_fields = ('nome', 'email')
    ordering = ('nome',)

@admin.register(PerfilVendedor)
class PerfilVendedorAdmin(admin.ModelAdmin):
    # Para exibir campos do Vendedor (OneToOne), criamos métodos auxiliares
    list_display = ('get_vendedor_nome', 'razao_social', 'get_vendedor_email', 'banco')
    search_fields = ('vendedor__nome', 'razao_social', 'vendedor__email')
    list_select_related = ('vendedor',) # Otimiza a consulta ao banco (evita N+1)

    # Método para pegar o nome e permitir ordenação
    @admin.display(description='Vendedor', ordering='vendedor__nome')
    def get_vendedor_nome(self, obj):
        return obj.vendedor.nome

    # Método para pegar o email
    @admin.display(description='E-mail do Vendedor', ordering='vendedor__email')
    def get_vendedor_email(self, obj):
        return obj.vendedor.email

class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 0 # Não cria linhas vazias extras

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_cliente_nome', 'status', 'data_pedido')
    list_filter = ('status', 'data_pedido') # Filtros laterais
    search_fields = ('id', 'cliente__nome', 'cliente__email')
    ordering = ('-data_pedido',)
    list_select_related = ('cliente',)
    inlines = [ItemPedidoInline] # Adiciona os itens do pedido na mesma tela

    @admin.display(description='Cliente', ordering='cliente__nome')
    def get_cliente_nome(self, obj):
        return obj.cliente.nome

@admin.register(ItemPedido)
class ItemPedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_pedido_id', 'get_produto_nome', 'quantidade', 'preco_unitario', 'get_subtotal')
    search_fields = ('pedido__id', 'produto__nome')
    list_select_related = ('pedido', 'produto') # Essencial para performance aqui

    @admin.display(description='ID Pedido', ordering='pedido__id')
    def get_pedido_id(self, obj):
        return f"#{obj.pedido.id}"

    @admin.display(description='Produto', ordering='produto__nome')
    def get_produto_nome(self, obj):
        return obj.produto.nome

    @admin.display(description='Subtotal')
    def get_subtotal(self, obj):
        return f"R$ {obj.subtotal}" # Acessa a @property do seu Model