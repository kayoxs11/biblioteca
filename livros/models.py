from django.db import models

class Usuario(models.Model):
    TIPOS = [
        ('aluno',     'Aluno'),
        ('professor', 'Professor'),
        ('externo',   'Usuário Externo'),
    ]

    nome      = models.CharField(max_length=100)
    sobrenome = models.CharField(max_length=100)
    email     = models.EmailField(unique=True)
    cpf       = models.CharField(max_length=14, unique=True)
    telefone  = models.CharField(max_length=15, blank=True)
    tipo      = models.CharField(max_length=20, choices=TIPOS)
    senha     = models.CharField(max_length=255)  # vai guardar criptografada

    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.nome} {self.sobrenome}'
    
    
class Livro(models.Model):
    GENEROS = [
        ('ficcao',     'Ficção'),
        ('nao_ficcao', 'Não-ficção'),
        ('romance',    'Romance'),
        ('aventura',   'Aventura'),
        ('ciencia',    'Ciência'),
        ('historia',   'História'),
        ('infantil',   'Infantil'),
        ('outros',     'Outros'),
    ]

    titulo     = models.CharField(max_length=200)
    autor      = models.CharField(max_length=200)
    isbn       = models.CharField(max_length=17, blank=True)
    ano        = models.IntegerField(null=True, blank=True)
    genero     = models.CharField(max_length=20, choices=GENEROS, blank=True)
    quantidade = models.IntegerField(default=1)
    sinopse    = models.TextField(blank=True)
    capa       = models.ImageField(upload_to='capas/', blank=True, null=True)

    cadastrado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo