-- Criando tabela alunos
CREATE TABLE alunos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    sobrenome TEXT NOT NULL,
    data_nascimento TEXT,
    endereco TEXT
);

-- Criando tabela professores
CREATE TABLE professores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    disciplina TEXT
);

-- Criando tabela cursos
CREATE TABLE cursos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    carga_horaria INTEGER
);

-- Criando tabela matriculas
CREATE TABLE matriculas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    aluno_id INTEGER,
    curso_id INTEGER,
    data_matricula TEXT,
    FOREIGN KEY (aluno_id) REFERENCES alunos(id),
    FOREIGN KEY (curso_id) REFERENCES cursos(id)
);

-- Inserindo dados
INSERT INTO alunos (nome, sobrenome, data_nascimento, endereco)
VALUES ('João', 'Silva', '2000-05-10', 'Rua A');

INSERT INTO professores (nome, disciplina)
VALUES ('Maria Souza', 'Matemática');

INSERT INTO cursos (nome, carga_horaria)
VALUES ('Banco de Dados', 60);

INSERT INTO matriculas (aluno_id, curso_id, data_matricula)
VALUES (1, 1, '2024-01-10');

-- Consultas
SELECT * FROM alunos;
SELECT * FROM cursos;
SELECT * FROM matriculas;
