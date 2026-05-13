from django.db import models
from django.utils import timezone


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
    senha     = models.CharField(max_length=255)

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


# ====================== NOVOS MODELOS ======================

class Reserva(models.Model):
    livro        = models.ForeignKey(Livro, on_delete=models.CASCADE, related_name='reservas')
    usuario      = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='reservas', null=True, blank=True)
    data_reserva = models.DateTimeField(auto_now_add=True)
    ativa        = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Reservas"
        ordering = ['-data_reserva']

    def __str__(self):
        return f"Reserva - {self.livro.titulo}"


class Emprestimo(models.Model):
    livro                   = models.ForeignKey(Livro, on_delete=models.CASCADE, related_name='emprestimos')
    usuario                 = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='emprestimos', null=True, blank=True)
    data_emprestimo         = models.DateTimeField(auto_now_add=True)
    data_devolucao_prevista = models.DateField()
    data_devolucao_real     = models.DateField(null=True, blank=True)
    devolvido               = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Empréstimos"
        ordering = ['-data_emprestimo']

    def __str__(self):
        return f"Empréstimo - {self.livro.titulo}"