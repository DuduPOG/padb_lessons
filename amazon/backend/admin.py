from django.contrib import admin
from .models import Cliente, Endereco, FormaPagamento, Item, Vendedor, Pedido

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
    
@admin.register(Vendedor)
class VendedorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'telefone')
    search_fields = ('nome', 'email')
    ordering = ('nome',)

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('data_pedido', 'data_entrega')
    search_fields = ('data_pedido', 'data_entrega')
    ordering = ('data_pedido',)