# Brain AG

## Overview

Este projeto é uma aplicação Django REST API desenvolvida para o desafio Brain Agriculture. A aplicação utiliza Django como framework web e PostgreSQL como banco de dados, com Python 3 como linguagem de programação.

## Features

- **Gestão de Produtores Rurais**: Criação, leitura, atualização e exclusão de registros de produtores rurais.
- **Dashboard**: Exibição de estatísticas sobre áreas agrícolas e vegetacionais, bem como a quantidade de propriedades por estado.
- **Manipulação de Culturas**: Registro e gerenciamento das culturas associadas a cada produtor rural.
- **Validação de Documentos**: Validação de CPF e CNPJ para garantir a integridade dos dados dos produtores.

## Installation

Para começar a usar este projeto, siga os passos abaixo:

1. **Clone o Repositório**

   ```bash
   git clone https://github.com/moreiralucas/brain-ag.git
   cd brain-ag
   ```

2. **Crie um Ambiente Virtual**

   ```bash
   python3 -m venv venv
   ```

3. **Ative o Ambiente Virtual**

   - No Windows:
     ```bash
     venv\Scripts\activate
     ```

   - No macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Instale as Dependências**

   ```bash
   pip install -r requirements.txt
   ```

5. **Execute as Migrações**

   ```bash
   python manage.py migrate
   ```

6. **Popula o banco de dados com dados fake**

   ```bash
   python manage.py populate_db
   ```

7. **Inicie o Servidor de Desenvolvimento**

   ```bash
   python manage.py runserver
   ```

   Sua aplicação estará disponível em `http://127.0.0.1:8000/`.

## Usage

1. **Endpoints de Produtores Rurais**: Utilize os endpoints `/rural-producers/` para gerenciar registros de produtores.
   - **GET** `/rural-producers/`: Listar todos os produtores.
   - **POST** `/rural-producers/`: Criar um novo produtor.
   - **GET** `/rural-producers/{id}/`: Visualizar detalhes de um produtor específico.
   - **PUT** `/rural-producers/{id}/`: Atualizar informações de um produtor específico.
   - **DELETE** `/rural-producers/{id}/`: Remover um produtor.

2. **Dashboard**: Acesse o endpoint `/dashboard/` para visualizar o dashboard com estatísticas sobre áreas e cultivos.
   - **GET** `/dashboard/`: Retorna estatísticas detalhadas, incluindo áreas agrícolas e vegetacionais e a quantidade de propriedades por estado.

## Requirements

- **Python 3.x**: A aplicação requer Python 3 para rodar.

As dependências do projeto estão listadas em `requirements.txt`.
