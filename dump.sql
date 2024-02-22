CREATE DATABASE dindin_python;

CREATE TABLE usuarios (
id serial not null primary key,
nome text not null,
email text unique not null,
senha text not null,
data_nascimento text,
telefone text,
cpf text unique not null
);

CREATE TABLE categorias (
id serial not null primary key,
descricao text not null
);

CREATE TABLE transacoes (
id serial not null primary key,
descricao text,
valor integer not null,
data text not null,
categoria_id integer not null references categorias(id),
usuario_id integer not null references usuarios(id),
tipo text not null
);



INSERT INTO categorias (descricao)
VALUES
('Alimentação'),
('Assinaturas e Serviços'),
('Casa'),
('Mercado'),
('Cuidados Pessoais'),
('Educação'),
('Família'),
('Lazer'),
('Pets'),
('Presentes'),
('Roupas'),
('Saúde'),
('Transporte'),
('Salário'),
('Vendas'),
('Outras receitas'),
('Outras despesas');