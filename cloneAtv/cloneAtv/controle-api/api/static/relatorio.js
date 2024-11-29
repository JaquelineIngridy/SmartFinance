document.addEventListener('DOMContentLoaded', function () {
    // Função para atualizar a tabela com transações do backend
    function updateTableFromBackend(transacoes) {
        const tbody = document.querySelector('#transaction-table tbody');
        tbody.innerHTML = ''; // Limpar a tabela antes de preencher

        let totalReceitas = 0;
        let totalDespesas = 0;

        transacoes.forEach(transacao => {
            const row = `
                <tr>
                    <td>${transacao.data}</td>
                    <td>${transacao.descricao}</td>
                    <td>R$ ${parseFloat(transacao.valor).toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</td>
                    <td>${transacao.categoria}</td>
                    <td>${transacao.tipo}</td>
                    <td>${transacao.metodo_pagamento}</td>
                    <td>${transacao.notas || ''}</td>
                </tr>
            `;
            tbody.innerHTML += row;

            // Atualizar totais
            if (transacao.tipo === 'Receita') {
                totalReceitas += parseFloat(transacao.valor);
            } else if (transacao.tipo === 'Despesa') {
                totalDespesas += parseFloat(transacao.valor);
            }
        });

        document.getElementById('totalReceitas').textContent = `R$${totalReceitas.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
        document.getElementById('totalDespesas').textContent = `R$${totalDespesas.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
        document.getElementById('balanco').textContent = `R$${(totalReceitas - totalDespesas).toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
    }

    // Carregar dados do backend
    fetch('/transacoes_json')
        .then(response => response.json())
        .then(transacoes => {
            updateTableFromBackend(transacoes);
        })
        .catch(error => console.error('Erro ao carregar transações:', error));
});


fetch('/transacoes_json')
    .then(response => response.json())
    .then(transacoes => {
        const tbody = document.querySelector('#transaction-table tbody');
        transacoes.forEach(transacao => {
            const row = `
                    <tr>
                        <td>${transacao.data}</td>
                        <td>${transacao.descricao}</td>
                        <td>R$ ${transacao.valor.toFixed(2)}</td>
                        <td>${transacao.categoria}</td>
                        <td>${transacao.tipo}</td>
                        <td>${transacao.metodo_pagamento}</td>
                        <td>${transacao.notas || ''}</td>
                    </tr>
                `;
            tbody.innerHTML += row;
        });
    })
    .catch(error => console.error('Erro ao carregar transações:', error));

