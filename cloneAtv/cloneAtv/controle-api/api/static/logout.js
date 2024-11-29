var menuItems = document.querySelectorAll('.item-menu');

function selectLink() {
    menuItems.forEach((item) => 
        item.classList.remove('ativo')
    );
    this.classList.add('ativo');
}

menuItems.forEach((item) => 
    item.addEventListener('click', selectLink)
);
// expandir menu
var btnExp = document.querySelector('#btn-exp');
var menuSide = document.querySelector('.menu_lateral');

btnExp.addEventListener('click', function() {
    menuSide.classList.toggle('expandir'); 
});
document.addEventListener('DOMContentLoaded', function() {
    const logoutButton = document.getElementById('logoutButton');
    
    logoutButton.addEventListener('click', function() {
        const confirmarLogout = confirm("Você realmente deseja sair do site?");
        if (confirmarLogout) {
            // Limpe os dados do localStorage se necessário
            localStorage.clear();
            // Redirecione para a página de login ou outra página desejada
            window.location.href = "/login/login.html";
        }
    });
});
