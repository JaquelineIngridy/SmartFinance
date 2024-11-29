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
document.addEventListener('DOMContentLoaded', function () {
    const goalForm = document.getElementById('goalForm');
    const goalTableBody = document.querySelector('#table tbody');
    const goals = JSON.parse(localStorage.getItem('goals')) || [];
    
    goalForm.addEventListener('submit', function (event) {
        event.preventDefault();
        const goal = {
            type: document.getElementById('goalType').value,
            amount: parseFloat(document.getElementById('goalAmount').value),
            date: document.getElementById('goalDate').value,
            progress: 0 // Valor inicial do progresso
        };
        goals.push(goal);
        localStorage.setItem('goals', JSON.stringify(goals));
        updateGoalTable();
        closePopup();
    });

    function updateGoalTable() {
        goalTableBody.innerHTML = '';
        goals.forEach((goal, index) => {
            const progressPercentage = ((goal.progress / goal.amount) * 100).toFixed(2);
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${goal.type}</td>
                <td>R$${goal.amount.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</td>
                <td>${goal.date}</td>
                <td>
                    <progress value="${goal.progress}" max="${goal.amount}"></progress>
                    R$${goal.progress.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                    (${progressPercentage}%)
                </td>
                <td>
                    <button onclick="updateGoal(${index})">Atualizar</button>
                    <button onclick="removeGoal(${index})">Remover</button>
                </td>
            `;
            goalTableBody.appendChild(row);
        });
    }

    window.updateGoal = function (index) {
        const progress = parseFloat(prompt('Quanto você adicionou para esta meta?'));
        if (!isNaN(progress) && progress > 0) {
            goals[index].progress += progress;
            if (goals[index].progress > goals[index].amount) goals[index].progress = goals[index].amount;
            localStorage.setItem('goals', JSON.stringify(goals));
            updateGoalTable();
        }
    };

    window.removeGoal = function (index) {
        goals.splice(index, 1);
        localStorage.setItem('goals', JSON.stringify(goals));
        updateGoalTable();
    };

    function closePopup() {
        document.getElementById('expensePopup').style.display = 'none';
        goalForm.reset();
    }

    function openPopup() {
        document.getElementById('expensePopup').style.display = 'block';
    }

    window.closePopup = closePopup;
    window.openPopup = openPopup;

    updateGoalTable();
});
