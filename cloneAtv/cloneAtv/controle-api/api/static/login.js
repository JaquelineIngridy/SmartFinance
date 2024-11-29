document.addEventListener('DOMContentLoaded', function() {
    const formLogin = document.getElementById('formLogin');
    formLogin.addEventListener('submit', function(event) {
        // Aqui você pode adicionar qualquer validação personalizada, se necessário
        // Por exemplo, verificar se os campos de e-mail e senha não estão vazios
        
        const email = document.getElementById('email').value.trim();
        const senha = document.getElementById('senha').value.trim();

        if (!email || !senha) {
            alert("Por favor, preencha todos os campos.");
        } else if (!email.includes("@gmail.com")) {
            alert("Por favor, insira um e-mail válido.");
        } else if (senha.length < 6) {
            alert("A senha deve ter pelo menos 6 caracteres.");
        } else {
            
            window.location.href = "{{ url_for('telaPrinc') }}"; 
        }
    });
});
