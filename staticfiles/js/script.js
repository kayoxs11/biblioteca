
// ---- Máscara CPF ----
document.getElementById('cpf').addEventListener('input', function () {
  let v = this.value.replace(/\D/g, '').slice(0, 11);
  v = v.replace(/(\d{3})(\d)/, '$1.$2');
  v = v.replace(/(\d{3})(\d)/, '$1.$2');
  v = v.replace(/(\d{3})(\d{1,2})$/, '$1-$2');
  this.value = v;
});

// ---- Máscara Telefone ----
document.getElementById('telefone').addEventListener('input', function () {
  let v = this.value.replace(/\D/g, '').slice(0, 11);
  if (v.length > 6) {
    v = v.replace(/^(\d{2})(\d{5})(\d{0,4})/, '($1) $2-$3');
  } else if (v.length > 2) {
    v = v.replace(/^(\d{2})(\d{0,5})/, '($1) $2');
  } else if (v.length > 0) {
    v = '(' + v;
  }
  this.value = v;
});

// ---- Mostrar / ocultar senha ----
function togglePwd(btnId, inputId) {
  document.getElementById(btnId).addEventListener('click', function () {
    const inp = document.getElementById(inputId);
    inp.type = inp.type === 'password' ? 'text' : 'password';
    this.textContent = inp.type === 'password' ? '👁️' : '🙈';
  });
}
togglePwd('toggleSenha', 'senha');
togglePwd('toggleConfirmar', 'confirmar');

// ---- Funções auxiliares de validação ----
function setError(id, msg) {
  const el  = document.getElementById(id + '-msg');
  const inp = document.getElementById(id);
  if (el)  { el.textContent = msg; el.className = 'msg error-msg'; }
  if (inp) { inp.classList.add('error'); }
}

function clearField(id) {
  const el  = document.getElementById(id + '-msg');
  const inp = document.getElementById(id);
  if (el)  { el.textContent = ''; el.className = 'msg'; }
  if (inp) { inp.classList.remove('error'); }
}

// ---- Validação de CPF (algoritmo oficial) ----
function validarCPF(cpf) {
  const nums = cpf.replace(/\D/g, '');
  if (nums.length !== 11 || /^(\d)\1+$/.test(nums)) return false;

  let soma = 0;
  for (let i = 0; i < 9; i++) soma += parseInt(nums[i]) * (10 - i);
  let r = (soma * 10) % 11;
  if (r === 10 || r === 11) r = 0;
  if (r !== parseInt(nums[9])) return false;

  soma = 0;
  for (let i = 0; i < 10; i++) soma += parseInt(nums[i]) * (11 - i);
  r = (soma * 10) % 11;
  if (r === 10 || r === 11) r = 0;
  return r === parseInt(nums[10]);
}

// ---- Envio do formulário ----
document.getElementById('cadastroForm').addEventListener('submit', function (e) {
  e.preventDefault(); // Impede o envio enquanto valida no front-end
  let ok = true;

  // Limpa erros anteriores
  ['nome', 'sobrenome', 'email', 'cpf', 'tipo', 'senha', 'confirmar'].forEach(clearField);

  // Lê os valores
  const nome      = document.getElementById('nome').value.trim();
  const sobrenome = document.getElementById('sobrenome').value.trim();
  const email     = document.getElementById('email').value.trim();
  const cpf       = document.getElementById('cpf').value.trim();
  const tipo      = document.getElementById('tipo').value;
  const senha     = document.getElementById('senha').value;
  const confirmar = document.getElementById('confirmar').value;
  const termos    = document.getElementById('termos').checked;

  // Validações
  if (!nome)                                          { setError('nome', 'Informe o nome.');            ok = false; }
  if (!sobrenome)                                     { setError('sobrenome', 'Informe o sobrenome.');  ok = false; }
  if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) { setError('email', 'E-mail inválido.');   ok = false; }
  if (!validarCPF(cpf))                               { setError('cpf', 'CPF inválido.');               ok = false; }
  if (!tipo)                                          { setError('tipo', 'Selecione o tipo.');          ok = false; }
  if (senha.length < 8)                               { setError('senha', 'Mínimo 8 caracteres.');      ok = false; }
  if (senha !== confirmar)                            { setError('confirmar', 'Senhas não coincidem.'); ok = false; }
  if (!termos) { alert('Aceite os termos para continuar.'); ok = false; }

  // Se tudo OK, envia de verdade pro Django
  if (ok) {
    this.submit();
  }
});