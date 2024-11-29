-- -- Criação do banco de dados
-- CREATE DATABASE Controle_Financeiro;
-- USE Controle_Financeiro;

-- -- Tabela Usuario
-- CREATE TABLE Usuario (
--    Id INT AUTO_INCREMENT PRIMARY KEY,
--    CPF VARCHAR(14) NOT NULL UNIQUE,
--    Nome VARCHAR(250) NOT NULL,
--    Email VARCHAR(100) NOT NULL UNIQUE,
--    Senha VARCHAR(255) NOT NULL,
--    DataNascimento DATE NOT NULL,
--    Sexo CHAR(1) NOT NULL CHECK (Sexo IN ('M', 'F')),
--    DataCriacao DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
--    DataAtualizacao DATETIME NULL,
--    DataFim DATETIME NULL
-- );

-- -- Inserir dados na tabela Usuario
-- INSERT INTO Usuario (CPF, Nome, Email, Senha, DataNascimento, Sexo) VALUES
-- ('123.456.789-00', 'Joao Silva', 'joao.silva@email.com', 'senha123', '1990-01-01', 'M'),
-- ('234.567.890-11', 'Maria Souza', 'maria.souza@email.com', 'senha123', '1992-02-15', 'F'),
-- ('345.678.901-22', 'Carlos Lima', 'carlos.lima@email.com', 'senha123', '1985-03-20', 'M'),
-- ('456.789.012-33', 'Ana Costa', 'ana.costa@email.com', 'senha123', '1995-04-10', 'F'),
-- ('567.890.123-44', 'Lucas Pereira', 'lucas.pereira@email.com', 'senha123', '1998-05-30', 'M');

-- -- Tabela TipoMovimentacao
-- CREATE TABLE TipoMovimentacao (
--    Id INT AUTO_INCREMENT PRIMARY KEY,
--    Codigo VARCHAR(50) NOT NULL UNIQUE,
--    Descricao VARCHAR(100) NOT NULL
-- );

-- -- Inserir dados na tabela TipoMovimentacao
-- INSERT INTO TipoMovimentacao (Codigo, Descricao) VALUES 
--    ('REC', 'Receita'),
--    ('DESP', 'Despesa');

-- -- Tabela Movimentacao
-- CREATE TABLE Movimentacao (
--    Id INT AUTO_INCREMENT PRIMARY KEY,
--    UsuarioId INT NOT NULL,
--    Categoria VARCHAR(100) NOT NULL,
--    Valor DECIMAL(18, 2) NOT NULL,
--    IdTipoMovimentacao INT NOT NULL, 
--    DataMovimentacao DATE NOT NULL,
--    DataPrevista DATE NULL,
--    Descricao VARCHAR(250) NOT NULL,
--    DataCriacao DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
--    DataFim DATETIME NULL,
--    DataAtualizacao DATETIME NULL,
--    FOREIGN KEY (UsuarioId) REFERENCES Usuario(Id),
--    FOREIGN KEY (IdTipoMovimentacao) REFERENCES TipoMovimentacao(Id)
-- );

-- -- Trigger para atualizar a DataAtualizacao
-- DELIMITER //
-- CREATE TRIGGER trgAtualizaMovimentacao
-- AFTER UPDATE ON Movimentacao
-- FOR EACH ROW
-- BEGIN
--    UPDATE Movimentacao
--    SET DataAtualizacao = CURRENT_TIMESTAMP
--    WHERE Id = NEW.Id;
-- END;
-- DELIMITER ;

-- -- Inserir dados na tabela Movimentacao
-- INSERT INTO Movimentacao (UsuarioId, Categoria, Valor, IdTipoMovimentacao, DataMovimentacao, DataPrevista, Descricao) 
-- VALUES
--    (1, 'Salário', 3000.00, 1, '2024-10-01', '2024-10-01', 'Salário de Outubro'),
--    (2, 'Salário', 4500.00, 1, '2024-10-05', '2024-10-05', 'Salário de Outubro'),
--    (3, 'Salário', 2800.00, 1, '2024-10-10', '2024-10-10', 'Salário de Outubro'),
--    (4, 'Salário', 3500.00, 1, '2024-10-15', '2024-10-15', 'Salário de Outubro'),
--    (5, 'Salário', 4000.00, 1, '2024-10-20', '2024-10-20', 'Salário de Outubro');

-- -- Tabela BalancoMensal
-- CREATE TABLE BalancoMensal (
--    Id INT AUTO_INCREMENT PRIMARY KEY,
--    UsuarioId INT NOT NULL,
--    MesReferencia DATE NOT NULL,
--    ReceitaTotal DECIMAL(18, 2) NOT NULL,
--    DespesasTotais DECIMAL(18, 2) NOT NULL,
--    SaldoInicial DECIMAL(18, 2) NOT NULL,
--    SaldoFinal DECIMAL(18, 2) NOT NULL,
--    FOREIGN KEY (UsuarioId) REFERENCES Usuario(Id)
-- );

-- -- Inserir dados na tabela BalancoMensal
-- INSERT INTO BalancoMensal(UsuarioId, MesReferencia, ReceitaTotal, DespesasTotais, SaldoInicial, SaldoFinal)
-- VALUES
--    (1, '2024-09-01', 3000.00, 1500.00, 1000.00, 2500.00),
--    (4, '2024-09-01', 4500.00, 2500.00, 500.00, 2500.00),
--    (5, '2024-09-01', 2800.00, 1800.00, 1500.00, 2500.00),
--    (3, '2024-09-01', 3500.00, 2000.00, 2000.00, 3500.00),
--    (2, '2024-09-01', 4000.00, 2500.00, 800.00, 2300.00);

-- -- Tabela OrcamentoMensal
-- CREATE TABLE OrcamentoMensal (
--    Id INT AUTO_INCREMENT PRIMARY KEY,
--    UsuarioId INT NOT NULL,
--    MesReferencia DATE NOT NULL,
--    ValorOrcamento DECIMAL(18, 2) NOT NULL,
--    ValorGasto DECIMAL(18, 2) NOT NULL,
--    DataCriacao DATE NOT NULL,
--    DataAtualizacao DATE NOT NULL,
--    FOREIGN KEY (UsuarioId) REFERENCES Usuario(Id)
-- );

-- -- Inserir dados na tabela OrcamentoMensal
-- INSERT INTO OrcamentoMensal(UsuarioId, MesReferencia, ValorOrcamento, ValorGasto, DataCriacao, DataAtualizacao)
-- VALUES
--    (4, '2024-09-01', 500.00, 200.00, '2024-08-01', '2024-09-01'),
--    (2, '2024-09-01', 800.00, 300.00, '2024-08-05', '2024-09-05'),
--    (3, '2024-09-01', 1000.00, 500.00, '2024-08-10', '2024-09-10'),
--    (1, '2024-09-01', 600.00, 400.00, '2024-08-15', '2024-09-15'),
--    (5, '2024-09-01', 300.00, 100.00, '2024-08-20', '2024-09-20');

-- -- Tabela Investimentos
-- CREATE TABLE Investimentos (
--    Id INT AUTO_INCREMENT PRIMARY KEY,
--    UsuarioId INT NOT NULL,
--    TipoInvestimento VARCHAR(100) NOT NULL,
--    ValorInvestido DECIMAL(18, 2) NOT NULL,
--    DataInvestido DATE NOT NULL,
--    ValorAtual DECIMAL(18, 2) NOT NULL,
--    FOREIGN KEY (UsuarioId) REFERENCES Usuario(Id)
-- );

-- -- Inserir dados na tabela Investimentos
-- INSERT INTO Investimentos(UsuarioId, TipoInvestimento, ValorInvestido, DataInvestido, ValorAtual) 
-- VALUES
--    (1, 'Ações', 2000.00, '2024-08-01', 2200.00),
--    (2, 'CDB', 3000.00, '2024-08-05', 3100.00),
--    (3, 'Fundos Imobiliários', 1500.00, '2024-08-10', 1600.00),
--    (4, 'Tesouro Direto', 1000.00, '2024-08-15', 1050.00),
--    (5, 'Poupança', 800.00, '2024-08-20', 820.00);

-- -- Tabela MetasFinanceiras
-- CREATE TABLE MetasFinanceiras (
--    Id INT AUTO_INCREMENT PRIMARY KEY,
--    UsuarioId INT NOT NULL,
--    DescricaoMeta VARCHAR(250) NOT NULL,
--    ValorMeta DECIMAL(18, 2) NOT NULL,
--    ValorAtual DECIMAL(18, 2) NOT NULL,
--    DataLimite DATE NOT NULL,
--    FOREIGN KEY (UsuarioId) REFERENCES Usuario(Id)
-- );

-- -- Inserir dados na tabela MetasFinanceiras
-- INSERT INTO MetasFinanceiras(UsuarioId, DescricaoMeta, ValorMeta, ValorAtual, DataLimite)
-- VALUES
--    (1, 'Comprar um carro', 30000.00, 5000.00, '2025-12-31'),
--    (2, 'Viajar para Europa', 20000.00, 10000.00, '2025-06-30'),
--    (3, 'Reformar a casa', 15000.00, 8000.00, '2025-10-31'),
--    (4, 'Abrir um negócio', 50000.00, 20000.00, '2025-05-31'),
--    (5, 'Pagar dívidas', 10000.00, 3000.00, '2025-03-31');

-- -- Alteração da coluna Senha para armazenar o hash da senha
-- UPDATE Usuario
-- SET Senha = SHA2(Senha, 256);

-- -- Criação da tabela de Histórico de Login
-- CREATE TABLE HistoricoLogin (
--    Id INT AUTO_INCREMENT PRIMARY KEY,
--    UsuarioId INT NOT NULL,
--    DataLogin DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
--    IPAddress VARCHAR(45) NULL,
--    FOREIGN KEY (UsuarioId) REFERENCES Usuario(Id)
-- );

-- -- Procedimento para autenticação do usuário
-- DELIMITER //
-- CREATE PROCEDURE AutenticarUsuario (IN Email VARCHAR(100), IN Senha VARCHAR(255))
-- BEGIN
--    DECLARE UsuarioId INT;
--    DECLARE SenhaHash VARBINARY(64);

--    -- Criar o hash da senha fornecida
--    SET SenhaHash = UNHEX(SHA2(Senha, 256));

--    -- Verificar se o usuário existe e a senha hash está correta
--    SELECT Id INTO UsuarioId
--    FROM Usuario
--    WHERE Email = Email AND Senha = SenhaHash;

--    IF UsuarioId IS NOT NULL THEN
--        -- Inserir no histórico de login
--        INSERT INTO HistoricoLogin (UsuarioId, IPAddress) 
--        VALUES (UsuarioId, NULL);

--        SELECT 'Login bem-sucedido' AS Mensagem, UsuarioId AS UsuarioId;
--    ELSE
--        SELECT 'Email ou senha incorretos' AS Mensagem;
--    END IF;
-- END //
-- DELIMITER ;

-- -- Teste da procedure
-- CALL AutenticarUsuario('joao.silva@email.com', 'senha123');
