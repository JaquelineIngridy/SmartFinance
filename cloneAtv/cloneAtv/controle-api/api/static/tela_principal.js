document.addEventListener('DOMContentLoaded', function () {
    // Selecionar Link do Menu
    var menuItems = document.querySelectorAll('.item-menu');
    function selectLink() {
        menuItems.forEach((item) => item.classList.remove('ativo'));
        this.classList.add('ativo');
    }
    menuItems.forEach((item) => item.addEventListener('click', selectLink));

    // Expandir Menu Lateral
    var btnExp = document.querySelector('#btn-exp');
    var menuSide = document.querySelector('.menu_lateral');
    btnExp.addEventListener('click', function () {
        menuSide.classList.toggle('expandir');
    });

    // Popup de Adicionar Conta
    const popup = document.getElementById('telaPopup');
    const closePopupButton = document.querySelector('.close');
    window.openPopup = function () {
        popup.style.display = 'block';
    }
    window.closePopup = function () {
        popup.style.display = 'none';
    }
    closePopupButton.addEventListener('click', function () {
        popup.style.display = 'none';
    });
    window.onclick = function (event) {
        if (event.target == popup) {
            popup.style.display = 'none';
        }
    }

    // Gerenciar Transações e Contas
    const transactions = JSON.parse(localStorage.getItem('transactions')) || [];
    const accounts = JSON.parse(localStorage.getItem('accounts')) || [];
    const gastosMensaisContainer = document.querySelector('.box:nth-child(2) ul');
    const accountList = document.getElementById('Lista');
    const saldoTotalElement = document.querySelector('.cabeca li:first-child .saldo');
    const receitasElement = document.querySelector('.cabeca li:nth-child(2) .saldo');
    const despesasElement = document.querySelector('.cabeca li:nth-child(3) .saldo');

    function formatCurrency(value) {
        return `R$ ${parseFloat(value).toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
    }

    function updateGastosMensais() {
        gastosMensaisContainer.innerHTML = '';
        transactions.forEach(transaction => {
            const li = document.createElement('li');
            li.textContent = `${transaction.date} - ${transaction.description} - ${formatCurrency(transaction.amount)} - Categoria: ${transaction.category}`;
            gastosMensaisContainer.appendChild(li);
        });
    }

    function updateAccountList() {
        accountList.innerHTML = '';
        accounts.forEach((account, index) => {
            const li = document.createElement('li');
            const bankNameSpan = document.createElement('span');
            bankNameSpan.textContent = `${account.bankName} (${account.accountType})`;
            bankNameSpan.classList.add('bank-name');
            const balanceSpan = document.createElement('span');
            balanceSpan.textContent = formatCurrency(account.balance);
            const deleteButton = document.createElement('button');
            deleteButton.textContent = 'x';
            deleteButton.onclick = function () {
                removeAccount(index);
            };
            li.appendChild(bankNameSpan);
            li.appendChild(balanceSpan);
            li.appendChild(deleteButton);
            accountList.appendChild(li);
        });
        updateTotals();
    }

    function updateTotals() {
        console.log("Atualizando Totais...");
        const receitasDasContas = accounts.reduce((total, account) => total + parseFloat(account.balance), 0);
        console.log("Receitas das Contas:", receitasDasContas);

        const receitasDeTransacoes = transactions
            .filter(t => t.type === 'Receita')
            .reduce((total, t) => total + parseFloat(t.amount), 0);
        console.log("Receitas das Transações:", receitasDeTransacoes);

        const receitas = receitasDasContas + receitasDeTransacoes;
        console.log("Receitas Totais:", receitas);

        const despesas = transactions
            .filter(t => t.type === 'Despesa')
            .reduce((total, t) => total + parseFloat(t.amount), 0);
        console.log("Despesas Totais:", despesas);

        const saldoTotal = receitas - despesas;
        console.log("Saldo Total:", saldoTotal);

        receitasElement.textContent = formatCurrency(receitas);
        despesasElement.textContent = formatCurrency(despesas);

        saldoTotalElement.textContent = formatCurrency(saldoTotal);
    }


    function removeAccount(index) {
        accounts.splice(index, 1);
        localStorage.setItem('accounts', JSON.stringify(accounts));
        updateAccountList();
    }

    // Função para adicionar conta no localStorage
    document.addEventListener('DOMContentLoaded', function () {
        // Verifique se o formulário está sendo selecionado corretamente
        const form = document.getElementById('telaForm');

        // Verifique se a seleção do formulário foi feita com sucesso
        if (form) {
            form.addEventListener('submit', function (event) {
                event.preventDefault();  // Impede o envio tradicional do formulário

                // Obtém os valores dos campos
                const bankName = document.getElementById('nome_banco').value;
                const balance = document.getElementById('balanco').value;
                const accountType = document.querySelector('input[name="accountType"]:checked').value;

                // Adiciona a conta
                addAccount(bankName, balance, accountType);
                closePopup();  // Fecha o pop-up após o envio
            });
        } else {
            console.error('Formulário não encontrado');
        }

        function updateAccountList() {
            const accounts = JSON.parse(localStorage.getItem('accounts')) || [];
            const accountList = document.getElementById('Lista');
            accountList.innerHTML = '';  // Limpa a lista existente

            accounts.forEach(account => {
                const li = document.createElement('li');
                li.textContent = `${account.bankName} - ${account.accountType} - Saldo: R$ ${account.balance.toFixed(2)}`;
                accountList.appendChild(li);
            });
        }

        // Inicializa a lista de contas ao carregar
        updateAccountList();
    });

    // Aqui, temos uma única função addAccount
    function addAccount(bankName, balance, accountType) {
        const newAccount = {
            bankName,
            balance: parseFloat(balance),  // Garantir que o saldo é um número
            accountType
        };

        let accounts = JSON.parse(localStorage.getItem('accounts')) || [];  // Certifique-se de pegar a lista atual de contas
        accounts.push(newAccount);
        localStorage.setItem('accounts', JSON.stringify(accounts));  // Atualize o localStorage
        updateAccountList();  // Atualiza a lista de contas na tela
    }


    updateGastosMensais();
    updateAccountList();
    updateTotals();

    // Metas Financeiras
    const goals = JSON.parse(localStorage.getItem('goals')) || [];
    const metasSaldoElement = document.querySelector('.cabeca li:nth-child(4) .saldo');

    function updateMetasSaldo() {
        // metasSaldoElement.innerHTML = '';
        goals.forEach(goal => {
            const progressPercentage = ((goal.progress / goal.amount) * 100).toFixed(2);
            const goalElement = document.createElement('div');
            goalElement.innerHTML = `
                <div>
                    Progresso: ${progressPercentage}% (R$${goal.progress.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })} de R$${goal.amount.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })})
                    <progress value="${goal.progress}" max="${goal.amount}"></progress>
                </div>
            `;
            metasSaldoElement.appendChild(goalElement);
        });
    }
    function removeAccount(accountId) {
        // Log para depuração - Verificar se o ID está correto
        console.log("Tentando remover a conta com ID:", accountId);

        // Encontra o item da conta com o id correspondente
        const accountItem = document.getElementById(`account-${accountId}`);

        // Se o item existir, remova ele da lista
        if (accountItem) {
            console.log("Conta encontrada. Removendo...");
            accountItem.remove();
        } else {
            console.log("Conta não encontrada. ID inválido ou já removido.");
        }
    }


});

fetch('/atualizar_dados', { method: 'POST' })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.getElementById('Saldo').textContent = `R$ ${data.saldo_total.toFixed(2)}`;
            document.getElementById('Receita').textContent = `R$ ${data.receita_total.toFixed(2)}`;
            document.getElementById('Despesa').textContent = `R$ ${data.despesa_total.toFixed(2)}`;
        } else {
            console.error(data.message);
        }
    })
    .catch(error => console.error('Erro:', error));
function atualizarDados() {
    fetch('/get_dados') // Rota que retorna os dados atualizados
        .then(response => response.json())
        .then(data => {
            const { receita_total, despesa_total, saldo_total } = data;

            // Atualizar valores na tela
            document.getElementById('receitasElement').textContent = `Receitas: R$ ${receita_total.toFixed(2)}`;
            document.getElementById('despesasElement').textContent = `Despesas: R$ ${despesa_total.toFixed(2)}`;
            document.getElementById('saldoTotalElement').textContent = `Saldo Total: R$ ${saldo_total.toFixed(2)}`;

            // Atualizar gráfico
            financeChart.data.datasets[0].data = [receita_total, despesa_total, saldo_total];
            financeChart.update();
        })
        .catch(error => console.error('Erro ao atualizar os dados:', error));
}




document.addEventListener('DOMContentLoaded', function () {
    const ctx = document.getElementById('transacoesPieChart').getContext('2d');

    // Função para obter os valores diretamente dos elementos HTML
    function getValuesFromScreen() {
        const receitaText = document.getElementById('Receita').textContent.trim();
        const despesaText = document.getElementById('Despesa').textContent.trim();
        const saldoText = document.getElementById('Saldo').textContent.trim();

        // Extrai os números dos textos (removendo "R$" e formatando corretamente)
        const receitas = parseFloat(receitaText.replace('R$', '').replace('','').replace(',', '.'));
        const despesas = parseFloat(despesaText.replace('R$', '').replace( '','').replace(',', '.'));
        const saldo = parseFloat(saldoText.replace('R$', '').replace( '','').replace(',', '.'));

        // Log para depuração
        console.log('Receitas:', receitas, 'Despesas:', despesas, 'Saldo:', saldo);

        return { receitas, despesas, saldo };
    }

    // Obtém os valores iniciais da tela
    const { receitas, despesas, saldo } = getValuesFromScreen();

    // Configuração inicial dos dados do gráfico
    const data = {
        labels: ['Receita', 'Despesa', 'Saldo'],
        datasets: [{
            label: 'Transações Financeiras',
            data: [receitas, despesas, saldo],
            backgroundColor: [
                'rgba(0, 128, 0)', // Verde para receitas
                'rgba(255, 0, 0)', // Vermelho para despesas
                'rgba(0, 0, 255)'  // Azul para saldo
            ],
            borderColor: [
                'rgba(0, 128, 0, 1)',
                'rgba(255, 0, 0, 1)',
                'rgba(0, 0, 255, 1)'
            ],
            borderWidth: 1
        }]
    };

    // Configuração do gráfico
    const config = {
        type: 'pie',
        data: data,
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            let label = context.label || '';
                            if (label) {
                                label += ': ';
                            }
                            if (context.parsed !== null) {
                                label += new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(context.parsed);
                            }
                            return label;
                        }
                    }
                }
            }
        },
    };

    // Cria o gráfico
    const transacoesPieChart = new Chart(ctx, config);

    // Atualiza os dados do gráfico com os valores atuais da tela
    function updateChart() {
        const { receitas, despesas, saldo } = getValuesFromScreen();
        transacoesPieChart.data.datasets[0].data = [receitas, despesas, saldo];
        transacoesPieChart.update();
    }

    // Observa alterações nos valores da tela para atualizar o gráfico
    setInterval(updateChart, 1000); // Atualiza o gráfico a cada segundo (ajuste conforme necessário)
});
