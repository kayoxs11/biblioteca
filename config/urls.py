"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from livros import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # === PÁGINAS PRINCIPAIS ===
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', views.login_view, name='login'),
    path('acervo/', views.acervo, name='acervo'),
    path('novo-livro/', views.novo_livro, name='novo_livro'),
    path('conta/', views.conta, name='conta'),
    path('gerenciar/', views.gerenciar, name='gerenciar'),
    path('cancelar-reserva/<int:reserva_id>/', views.cancelar_reserva, name='cancelar_reserva'),
    path('converter-reserva/<int:reserva_id>/', views.converter_reserva, name='converter_reserva'),
    
    # === NOVAS ROTAS (Empréstimo e Reserva) ===
    path('reservar/<int:livro_id>/', views.reservar_livro, name='reservar_livro'),
    path('emprestar/<int:livro_id>/', views.emprestar_livro, name='emprestar_livro'),
    path('devolver/<int:emprestimo_id>/', views.devolver_livro, name='devolver_livro'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)