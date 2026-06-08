from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages 
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.hashers import make_password, check_password
from .models import Usuario, Livro, Reserva, Emprestimo


# ====================== NOVO LIVRO ======================
def novo_livro(request):
    if request.method == 'POST':
        try:
            ano = request.POST.get('ano')
            quantidade = request.POST.get('quantidade')

            Livro.objects.create(
                titulo     = request.POST.get('titulo'),
                autor      = request.POST.get('autor'),
                isbn       = request.POST.get('isbn', ''),
                ano        = int(ano) if ano and ano.strip().isdigit() else None,
                genero     = request.POST.get('genero', ''),
                quantidade = int(quantidade) if quantidade and quantidade.strip().isdigit() else 1,
                sinopse    = request.POST.get('sinopse', ''),
                capa       = request.FILES.get('capa'),
            )
            messages.success(request, '✅ Livro cadastrado com sucesso!')
            return redirect('acervo')
        
        except Exception as e:
            messages.error(request, f'Erro ao salvar: {e}')
            return render(request, 'livros/novo_livro.html')

    return render(request, 'livros/novo_livro.html')


# ====================== ACERVO ======================
def acervo(request):
    livros = Livro.objects.all()

    # Total de títulos cadastrados
    total_titulos = livros.count()

    # Soma real dos livros disponíveis no estoque
    disponiveis = sum(livro.quantidade for livro in livros)

    # Quantidade de reservas ativas
    reservados = Reserva.objects.filter(ativa=True).count()

    # Quantidade de empréstimos ativos
    emprestados = Emprestimo.objects.filter(devolvido=False).count()

    context = {
        'livros': livros,
        'total': total_titulos,
        'disponiveis': disponiveis,
        'emprestados': emprestados,
        'reservados': reservados,
    }

    return render(request, 'livros/acervo.html', context)
# ====================== RESERVAR ======================
def reservar_livro(request, livro_id):
    livro = get_object_or_404(Livro, id=livro_id)
    
    if request.method == 'POST':
        if livro.quantidade > 0:
            livro.quantidade -= 1
            livro.save()
            Reserva.objects.create(livro=livro)
            messages.success(request, f'✅ "{livro.titulo}" reservado!')
            return redirect('acervo')
        else:
            messages.error(request, 'Este livro não está disponível.')
    
    return render(request, 'livros/reservar_livro.html', {'livro': livro})


# ====================== EMPRESTAR ======================
def emprestar_livro(request, livro_id):
    livro = get_object_or_404(Livro, id=livro_id)
    
    if request.method == 'POST':
        if livro.quantidade > 0:
            data_devolucao = request.POST.get('data_devolucao')
            
            livro.quantidade -= 1
            livro.save()

            Emprestimo.objects.create(
                livro=livro,
                data_devolucao_prevista=data_devolucao,
            )
            messages.success(request, f'✅ "{livro.titulo}" emprestado!')
            return redirect('acervo')
        else:
            messages.error(request, 'Este livro não está disponível.')
    
    return render(request, 'livros/emprestar_livro.html', {'livro': livro})


# ====================== CADASTRO E LOGIN ======================
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
            nome=nome, sobrenome=sobrenome, email=email,
            cpf=cpf, telefone=telefone, tipo=tipo,
            senha=make_password(senha)
        )
        messages.success(request, 'Usuário cadastrado com sucesso!')
        return redirect('login')

    return render(request, 'livros/cadastro.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        try:
            usuario = Usuario.objects.get(email=email)

            if check_password(senha, usuario.senha):
                request.session['usuario_id'] = usuario.id
                request.session['usuario_nome'] = usuario.nome

                messages.success(request, f'Bem-vindo, {usuario.nome}!')
                return redirect('acervo')
            else:
                messages.error(request, 'Senha incorreta.')

        except Usuario.DoesNotExist:
            messages.error(request, 'E-mail não encontrado.')

    return render(request, 'livros/login.html')


def conta(request):
    usuario_id = request.session.get('usuario_id')

    if not usuario_id:
        return redirect('login')

    usuario = get_object_or_404(Usuario, id=usuario_id)

    return render(request, 'livros/conta.html', {
        'usuario': usuario
    })


# ====================== GERENCIAMENTO ======================
def gerenciar(request):
    reservas = Reserva.objects.filter(ativa=True).select_related('livro')
    emprestimos = Emprestimo.objects.filter(devolvido=False).select_related('livro')
    
    context = {
        'reservas': reservas,
        'emprestimos': emprestimos,
    }
    return render(request, 'livros/gerenciar.html', context)


# ====================== CANCELAR RESERVA ======================
def cancelar_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    livro = reserva.livro
    
    livro.quantidade += 1
    livro.save()
    
    reserva.ativa = False
    reserva.save()
    
    messages.success(request, f'Reserva do livro "{livro.titulo}" cancelada com sucesso.')
    return redirect('gerenciar')


# ====================== CONVERTER RESERVA PARA EMPRÉSTIMO ======================
def converter_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    livro = reserva.livro
    
    if request.method == 'POST':
        data_devolucao = request.POST.get('data_devolucao')
        
        Emprestimo.objects.create(
            livro=livro,
            data_devolucao_prevista=data_devolucao,
        )
        
        reserva.ativa = False
        reserva.save()
        
        messages.success(request, f'Reserva convertida em empréstimo com sucesso!')
        return redirect('gerenciar')
    
    return render(request, 'livros/converter_reserva.html', {'reserva': reserva, 'livro': livro})


# ====================== DEVOLVER ======================
def devolver_livro(request, emprestimo_id):
    emprestimo = get_object_or_404(Emprestimo, id=emprestimo_id)
    
    if not emprestimo.devolvido:
        emprestimo.devolvido = True
        emprestimo.data_devolucao_real = timezone.now().date()
        emprestimo.livro.quantidade += 1
        emprestimo.livro.save()
        emprestimo.save()
        
        messages.success(request, f'✅ "{emprestimo.livro.titulo}" devolvido com sucesso!')
    
    return redirect('gerenciar')

def conta(request):
    try:
        usuario = Usuario.objects.first()  # temporário até ter login completo
        return render(request, 'livros/conta.html', {'usuario': usuario})
    except:
        return render(request, 'livros/conta.html', {})