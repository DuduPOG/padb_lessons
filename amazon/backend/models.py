from django.db import models

# Create your models here.

class Cliente(models.Model):

    nome = models.CharField(max_length=100, null=False, blank=False)
    email = models.EmailField(unique=True, null=False, blank=False) # UNIQUE no banco
    telefone = models.CharField(max_length=20, blank=True)
    data_cadastro = models.DateTimeField(auto_now_add=True, null=False, blank=False) # Preenchido automaticamente
    
    class Meta:
        db_table = 'clientes' # Nome explícito da tabela no banco
        ordering = ['nome'] # Ordenação padrão nas consultas
    
    def __str__(self):
        # Retorna a representação legível do objeto
        return f'{self.nome} <{self.email}>'
    
class Endereco(models.Model):
    #cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    rua = models.CharField(max_length=100, null=False, blank=False)
    numero = models.CharField(max_length=10, null=False, blank=False)
    bairro = models.CharField(max_length=50, null=False, blank=False)
    cidade = models.CharField(max_length=50, null=False, blank=False)
    estado = models.CharField(max_length=2, null=False, blank=False) 
    cep = models.CharField(max_length=10, null=False, blank=False)

    def __str__(self):
        return f'{self.rua}, {self.numero} - {self.bairro}, {self.cidade}/{self.estado} - {self.cep}'
    
class Item (models.Model):
    nome = models.CharField(max_length=100, null=False, blank=False)
    descricao = models.CharField(max_length=100, null=False, blank=True)
    preco = models.DecimalField(max_digits=8, decimal_places=2, null=False, blank=False)
    estoque = models.IntegerField()
    
    def __str__(self):
        return f'{self.nome} - {self.descricao} - R$ {self.preco} - Estoque: {self.estoque}'
    
class FormaPagamento(models.Model):
    descricao = models.CharField(max_length=100, null=False, blank=False)
    
    def __str__(self):
        return self.descricao
    
class Vendedor(models.Model):
    nome = models.CharField(max_length=100, null=False, blank=False)
    email = models.EmailField(unique=True, null=False, blank=False)
    cpf_cnpj = models.CharField(max_length=18, unique=True, null=False, blank=False)
    telefone = models.CharField(max_length=15, null=False, blank=True)
    avaliacao = models.DecimalField(max_digits=3, decimal_places=2, default=5.00, null=False, blank=False)
    ativo = models.BooleanField(default=True, null=False, blank=False)
    data_cadastro = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    
    class Meta:
        db_table = 'vendedores'
        ordering = ['nome']
    
    def __str__(self):
        return f'{self.nome} ({self.cpf_cnpj})'
    
class Produto(models.Model):
    CATEGORIA_CHOICES = [
        ('eletronicos', 'Eletrônicos'),
        ('roupas', 'roupas e Acessórios'),
        ('livros', 'Livros'),
        ('alimentos', 'Alimentos'),
        ('outros', 'Outros'), 
    ]
    nome = models.CharField(max_length=200, null=False, blank=False)
    descricao = models.TextField(blank=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    estoque = models.IntegerField(default=0, null=False, blank=False)
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES, default='outros', null=False, blank=False)
    disponivel = models.BooleanField(default=True, null=False, blank=False)
    criado_em = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    atualizado_em = models.DateTimeField(auto_now=True, null=False, blank=False) # Atualizado a cada save()
    
    class Meta:
        db_table = 'produtos'
        ordering = ['nome']
    
    def __str__(self):
        return f'[{self.nome} — R$ {self.preco}'
    
class Pedido(models.Model):
    #cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    #vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE)
    #endereco_entrega = models.ForeignKey(Endereco, on_delete=models.CASCADE)
    #itens = models.ManyToManyField(Item)
    #forma_pagamento = models.ForeignKey(FormaPagamento, on_delete=models.CASCADE)
    data_pedido = models.DateTimeField(auto_now_add=True)
    data_entrega = models.DateTimeField()
    
    def __str__(self):
        return f'{self.cliente} - {self.vendedor} - {self.data_pedido}'