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
    
class PerfilVendedor(models.Model):
    vendedor = models.OneToOneField(
        Vendedor,
        on_delete=models.CASCADE,
        related_name='perfil',
        primary_key=True # usa o id do vendedor como PK
    )
    razao_social = models.CharField(max_length=150, blank=True)
    inscricao_estadual = models.CharField(max_length=20, blank=True)
    banco = models.CharField(max_length=50, blank=True)
    agencia = models.CharField(max_length=10, blank=True)
    conta = models.CharField(max_length=20, blank=True)
    chave_pix = models.CharField(max_length=100, blank=True)
    
    class Meta:
        db_table = 'perfis_vendedores'
        ordering = ['vendedor']
        
    def __str__(self):
        return f'Perfil de {self.vendedor.nome}'
    
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
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('pago', 'Pago'),
        ('enviado', 'Enviado'),
        ('entregue', 'Entregue'),
        ('cancelado', 'Cancelado'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='pedidos')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    #vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE)
    #endereco_entrega = models.ForeignKey(Endereco, on_delete=models.CASCADE)
    #itens = models.ManyToManyField(Item)
    #forma_pagamento = models.ForeignKey(FormaPagamento, on_delete=models.CASCADE)
    data_pedido = models.DateTimeField(auto_now_add=True)
    observacoes = models.TextField(blank=True)
    #data_entrega = models.DateTimeField()
    
    
    class Meta:
        db_table = 'pedidos'
        ordering = ['-data_pedido']
    
    def __str__(self):
        return f'Pedido #{self.id} — {self.cliente.nome}'

class ItemPedido(models.Model):
    pedido = models.ForeignKey(
                Pedido,
                on_delete=models.CASCADE, # itens não existem sem o pedido
                related_name='itens'
            )
    produto = models.ForeignKey(
                Produto,
                on_delete=models.PROTECT, # produto com vendas não pode ser apagado
                related_name='itens_vendidos'
            )
    quantidade = models.PositiveIntegerField(default=1)
    preco_unitario = models.DecimalField(
                        max_digits=10,
                        decimal_places=2,
                        help_text='Preço congelado no momento da compra'
                    )
    
    class Meta:
        db_table = 'itens_pedido'
        unique_together = ['pedido', 'produto'] # mesmo produto não duplica no pedido
        
    def __str__(self):
        return f'{self.quantidade}x {self.produto.nome}'
    
    @property
    def subtotal(self):
        return self.quantidade * self.preco_unitario
