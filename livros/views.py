from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from .models import Usuario, Livro

def novo_livro(request):
    if request.method == 'POST':
        Livro.objects.create(
            titulo     = request.POST.get('titulo'),
            autor      = request.POST.get('autor'),
            isbn       = request.POST.get('isbn', ''),
            ano        = request.POST.get('ano') or None,
            genero     = request.POST.get('genero', ''),
            quantidade = request.POST.get('quantidade', 1),
            sinopse    = request.POST.get('sinopse', ''),
            capa       = request.FILES.get('capa'),
        )
        return redirect('acervo')

    return render(request, 'livros/novo_livro.html')

def acervo(request):
    livros = Livro.objects.all()
    return render(request, 'livros/acervo.html', {'livros': livros})

def cadastro(request):
    if request.method == 'POST':
        nome      = request.POST.get('nome')
        sobrenome = request.POST.get('sobrenome')
        email     = request.POST.get('email')
        cpf       = request.POST.get('cpf')
        telefone  = request.POST.get('telefone')
        tipo      = request.POST.get('tipo')
        senha     = request.POST.get('senha')

        Usuario.objects.create(
            nome      = nome,
            sobrenome = sobrenome,
            email     = email,
            cpf       = cpf,
            telefone  = telefone,
            tipo      = tipo,
            senha     = make_password(senha)
        )
        return redirect('cadastro')

from django.contrib.auth.hashers import check_password

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        try:
            usuario = Usuario.objects.get(email=email)
            if check_password(senha, usuario.senha):
                return redirect('acervo')
            else:
                return render(request, 'livros/login.html', {'erro': 'Senha incorreta.'})
        except Usuario.DoesNotExist:
            return render(request, 'livros/login.html', {'erro': 'E-mail não encontrado.'})

    return render(request, 'livros/login.html')

    return render(request, 'livros/cadastro.html')

def acervo(request):
    return render(request, 'livros/acervo.html')

def novo_livro(request):
    return render(request, 'livros/novo_livro.html')

def conta(request):
    return render(request, 'livros/conta.html')