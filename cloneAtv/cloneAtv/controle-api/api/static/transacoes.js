document.addEventListener('DOMContentLoaded', function () {
    // Função para carregar transações do backend e exibi-las
    function loadTransactions() {
        fetch('/transacoes')
            .then(response => response.json())
            .then(data => {
                const transactionTableBody = document.querySelector('#transactionTableBody');
                const gastosMensaisList = document.getElementById('gastos-mensais-list');

                transactionTableBody.innerHTML = ''; 
                gastosMensaisList.innerHTML = '';
                
                data.forEach(transaction => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${transaction.data}</td>
                        <td>${transaction.descricao}</td>
                        <td>R$${parseFloat(transaction.valor).toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</td>
                        <td>${transaction.categoria}</td>
                        <td>${transaction.tipo}</td>
                        <td>${transaction.metodo_pagamento}</td>
                        <td>${transaction.notas}</td>
                        <td><button onclick="removeTransaction(${data.indexOf(transaction)})">Excluir</button></td>
                    `;
                    transactionTableBody.appendChild(row);
                });
            })
            .catch(error => console.error('Erro ao carregar as transações:', error));
    }

    // Função de envio de formulário
    const transactionForm = document.getElementById('expenseForm');
    transactionForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const transaction = {
            data: new Date().toISOString().split('T')[0], // Define a data atual em formato 'YYYY-MM-DD'
            descricao: document.getElementById('descricao').value,
            valor: document.getElementById('valor').value,
            categoria: document.getElementById('categoria').value,
            tipo: document.getElementById('tipo').value,
            metodo_pagamento: document.getElementById('metodo_pagamento').value,
            notas: document.getElementById('notas').value || ''
        };

        // Envia a transação para o servidor
        fetch('/transacoes', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(transaction)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                loadTransactions();  // Atualiza a tabela de transações
                transactionForm.reset(); // Reseta os campos do formulário
                closeExpensePopup(); // Fecha o pop-up
            } else {
                alert('Erro ao adicionar transação');
            }
        })
        .catch(error => console.error('Erro na requisição:', error));
    });

    // Funções para abrir e fechar o pop-up de adicionar transação
    function closeExpensePopup() {
        const popup = document.getElementById('expensePopup');
        if (popup) {
            popup.style.display = 'none';
        } else {
            console.error('Elemento expensePopup não encontrado.');
        }
    }

    function openExpensePopup() {
        const popup = document.getElementById('expensePopup');
        if (popup) {
            popup.style.display = 'block';
        } else {
            console.error('Elemento expensePopup não encontrado.');
        }
    }

    // Adiciona eventos ao botão para abrir e fechar o popup
    const openPopupButton = document.getElementById('openPopupButton');
    if (openPopupButton) {
        openPopupButton.addEventListener('click', openExpensePopup);
    } else {
        console.error('Botão openPopupButton não encontrado.');
    }

    const closePopupButton = document.querySelector('.close');
    if (closePopupButton) {
        closePopupButton.addEventListener('click', closeExpensePopup);
    } else {
        console.error('Botão closePopupButton não encontrado.');
    }

    // Disponibiliza as funções no escopo global
    window.loadTransactions = loadTransactions; 
    window.removeTransaction = removeTransaction;
    window.closeExpensePopup = closeExpensePopup;
    window.openExpensePopup = openExpensePopup;

    // Carregar transações ao iniciar a página
    loadTransactions();
});
// Função para atualizar os totais e o gráfico de pizza
function updateTotals() {
    // Calcular a receita das transações (considerando transações do tipo 'Receita')
    const receita_total = transactions.filter(t => t.type === 'Receita')
                            .reduce((total, t) => total + parseFloat(t.amount), 0);

    // Calcular as despesas (considerando transações do tipo 'Despesa')
    const despesa_total = transactions.filter(t => t.type === 'Despesa')
                            .reduce((total, t) => total + parseFloat(t.amount), 0);

    // Calcular o saldo das contas
    const saldoContas = accounts.reduce((total, account) => total + parseFloat(account.balance), 0);

    // Calcular o saldo total (considerando receita total e despesas)
    const saldo_total = saldoContas + receita_total - despesa_total;

    // Atualizar os valores na tela
    receitasElement.textContent = `Receitas: ${formatCurrency(receita_total)}`;
    despesasElement.textContent = `Despesas: ${formatCurrency(despesa_total)}`;
    saldoTotalElement.textContent = `Saldo Total: ${formatCurrency(saldo_total)}`;

    // Atualizar o gráfico com os novos dados
    updateChartData(receita_total, despesa_total, saldo_total);
}

// Chamar a função para atualizar os totais e o gráfico ao carregar a página
updateTotals();


    function addTransactionRow(transacao) {
        const tableBody = document.getElementById('transactionTableBody');
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${new Date(transacao.data).toLocaleDateString()}</td>
            <td>${transacao.descricao}</td>
            <td>R$ ${transacao.valor.toFixed(2)}</td>
            <td>${transacao.categoria}</td>
            <td>${transacao.tipo}</td>
            <td>${transacao.metodo_pagamento}</td>
            <td>${transacao.notas || 'Sem notas'}</td>
            <td><button class="btn-delete" onclick="deleteTransaction(${transacao.id})">Excluir</button></td>
        `;
        tableBody.appendChild(row);
    }


