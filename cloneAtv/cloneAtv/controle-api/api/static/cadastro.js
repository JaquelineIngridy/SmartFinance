document.addEventListener('DOMContentLoaded', function () {
    console.log('DOM carregado');
    
    const formCadastro = document.getElementById('formCadastro');
    console.log('Formulário encontrado:', formCadastro);
    
    formCadastro.addEventListener('submit', function (event) {
      console.log('Formulário submetido'); // Verifique se isso aparece no console
    });
      
      event.preventDefault();
      
      const nome = document.getElementById('nome').value.trim();
      const email = document.getElementById('email').value.trim();
      const cpf = document.getElementById('cpf').value.trim();
      const datanasc = document.getElementById('datanasc').value.trim();
      const sexo = document.getElementById('sexo').value.trim();
      const senha = document.getElementById('senha').value.trim();
      
      console.log('Campos:', nome, email, cpf, datanasc, sexo, senha);
      
      if (!nome || !email || !cpf || !datanasc || !sexo || !senha) {
        alert('Por favor, preencha todos os campos corretamente.');
        return;
      }
      
      // Envia o formulário
      fetch('/cadastro', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          nome,
          email,
          cpf,
          datanasc,
          sexo,
          senha
        })
      })
      .then(response => response.json())
      .then(data => console.log(data))
      .catch(error => console.error(error));
    });