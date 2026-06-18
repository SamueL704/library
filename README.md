# Sistema de Gerenciamento de Empréstimos de Biblioteca

API REST para gerenciamento de empréstimos de exemplares físicos de livros em uma biblioteca.

O projeto foi desenvolvido como atividade acadêmica de Backend com FastAPI. O foco principal não é apenas criar um CRUD, mas modelar um domínio com regras de negócio, estados de ciclo de vida, cálculos derivados, consistência de dados, migrations incrementais e decisões de design justificáveis.

## 1. Descrição do domínio

O sistema representa uma biblioteca que possui usuários cadastrados, livros, exemplares físicos, empréstimos e multas.

Um livro representa a obra bibliográfica, como título, autor e descrição. Porém, o empréstimo não acontece diretamente sobre o livro, e sim sobre um exemplar físico. Isso permite controlar cada cópia separadamente.

Um usuário pode realizar empréstimos desde que existam exemplares disponíveis, que ele não tenha multas pendentes e que não tenha ultrapassado o limite máximo de empréstimos ativos.

Quando um empréstimo passa da data prevista de devolução, o sistema pode marcar o empréstimo como atrasado e gerar uma multa. A multa permanece pendente até ser paga.

Nesta primeira versão, as reservas não serão implementadas. Essa funcionalidade foi deixada para uma implementação futura.

## 2. Diagrama ER

```text
USUARIO
  id PK
  nome
  email UNIQUE
  senha
    │
    │ 1:N
    ▼
EMPRESTIMO
  id PK
  usuario_id FK
  exemplar_id FK
  data_emprestimo
  devolucao_prevista
  data_devolucao
  status
    │
    │ 1:1
    ▼
MULTA
  id PK
  usuario_id FK
  emprestimo_id FK UNIQUE
  valor
  status


LIVRO
  id PK
  titulo
  autor
  descricao
    │
    │ 1:N
    ▼
EXEMPLAR
  id PK
  livro_id FK
  status
    │
    │ 1:N
    ▼
EMPRESTIMO


EMPRESTIMO
    │
    │ 1:N
    ▼
LOG_EMPRESTIMO
  id PK
  emprestimo_id FK
  acao
  data_evento
```

## 3. Como rodar localmente

### 3.1. Pré-requisitos

- Python 3.12 ou superior
- Docker
- Docker Compose
- Git

### 3.2. Clonar o repositório

```bash
git clone https://github.com/SamueL704/library.git
cd library
```

### 3.3. Criar o arquivo `.env`

Crie um arquivo `.env` na raiz do projeto com base no `.env.example`.

Exemplo para rodar a API dentro do Docker:

```env
POSTGRES_DB=biblioteca_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

DATABASE_URL=postgresql+psycopg://postgres:postgres@db:5432/biblioteca_db

SECRET_KEY=sua_chave_secreta
PORT=8000
```

Exemplo para rodar a API localmente e apenas o banco no Docker:

```env
POSTGRES_DB=biblioteca_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/biblioteca_db

SECRET_KEY=sua_chave_secreta
PORT=8000
```

Quando a API roda dentro do Docker, o host do banco é `db`, pois esse é o nome do serviço no `docker-compose.yml`.

Quando a API roda diretamente no computador, o host do banco é `localhost`.

### 3.4. Subir os containers

Para subir API, banco e Adminer:

```bash
docker compose up --build
```

Para subir em segundo plano:

```bash
docker compose up --build -d
```

Para parar os containers:

```bash
docker compose down
```

Para parar os containers e apagar o volume do banco:

```bash
docker compose down -v
```

Atenção: `docker compose down -v` apaga os dados salvos no volume do PostgreSQL.

### 3.5. Acessos

API:

```text
http://localhost:8000
```

Swagger:

```text
http://localhost:8000/docs
```

Adminer:

```text
http://localhost:8080
```

Dados para acessar o Adminer:

```text
Sistema: PostgreSQL
Servidor: db
Usuário: postgres
Senha: postgres
Banco: biblioteca_db
```

## 4. Estrutura planejada do projeto

```text
library/
├── app/
│   ├── main.py
│   ├── core/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── repositories/
│   └── routers/
├── alembic/
│   ├── versions/
│   └── env.py
├── tests/
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── alembic.ini
├── requirements.txt
└── README.md
```


## 5. Modelagem de entidades

### 5.1. Usuário

Representa um usuário cadastrado na biblioteca apto a realizar empréstimos.

| Campo | Tipo | Obrigatório | Restrições |
|---|---|---|---|
| id | Integer | Sim | PK |
| nome | String | Sim | Não vazio |
| email | String | Sim | Único |
| senha | String | Sim | Hash |

Relacionamentos:

Um usuário pode realizar vários empréstimos ao longo do tempo. Cada empréstimo pertence a apenas um usuário.

Um usuário também pode acumular várias multas referentes a diferentes empréstimos atrasados. Cada multa pertence a apenas um usuário.

Cardinalidades:

```text
Usuario 1:N Emprestimo
Usuario 1:N Multa
```

### 5.2. Livro

Representa as informações bibliográficas de um livro.

| Campo | Tipo | Obrigatório | Restrições |
|---|---|---|---|
| id | Integer | Sim | PK |
| titulo | String | Sim | Não vazio |
| autor | String | Sim | Não vazio |
| descricao | String | Não | Opcional |

Relacionamentos:

Um livro representa uma obra bibliográfica. Os exemplares representam as cópias físicas dessa obra. Portanto, um livro pode possuir vários exemplares, mas cada exemplar pertence a apenas um livro.

Cardinalidade:

```text
Livro 1:N Exemplar
```

Observação:

A quantidade de exemplares disponíveis não será armazenada diretamente na tabela `livros`. A disponibilidade será calculada a partir dos exemplares com status `DISPONIVEL`.

### 5.3. Exemplar

Representa uma cópia física específica de um livro.

| Campo | Tipo | Obrigatório | Restrições |
|---|---|---|---|
| id | Integer | Sim | PK |
| livro_id | Integer | Sim | FK Livro |
| status | Enum | Sim | DISPONIVEL, EMPRESTADO |

Relacionamentos:

Vários exemplares podem pertencer ao mesmo livro.

Um exemplar pode ser emprestado diversas vezes ao longo de sua vida útil, gerando vários registros de empréstimo. Porém, cada empréstimo se refere a apenas um exemplar.

Cardinalidades:

```text
Exemplar N:1 Livro
Exemplar 1:N Emprestimo
```

Máquina de estados:

```text
DISPONIVEL
    │
    ▼
EMPRESTADO
    │
    ▼
DISPONIVEL
```

O estado do exemplar não possui estado terminal, pois o mesmo exemplar pode ser emprestado e devolvido diversas vezes.

### 5.4. Empréstimo

Representa o empréstimo de um exemplar para um usuário.

| Campo | Tipo | Obrigatório | Restrições |
|---|---|---|---|
| id | Integer | Sim | PK |
| usuario_id | Integer | Sim | FK Usuário |
| exemplar_id | Integer | Sim | FK Exemplar |
| data_emprestimo | Date | Sim | Obrigatória |
| devolucao_prevista | Date | Sim | Obrigatória |
| data_devolucao | Date | Não | Opcional |
| status | Enum | Sim | ATIVO, ATRASADO, FINALIZADO |

Relacionamentos:

Um empréstimo pertence a um usuário.

Um empréstimo se refere a um exemplar.

Um empréstimo pode gerar no máximo uma multa por atraso.

Cardinalidades:

```text
Emprestimo N:1 Usuario
Emprestimo N:1 Exemplar
Emprestimo 1:1 Multa
```

Máquina de estados:

```text
ATIVO ───────────► FINALIZADO
  │
  ▼
ATRASADO ───────► FINALIZADO
```

O estado `FINALIZADO` é terminal. Após a devolução do exemplar, não faz sentido retornar o empréstimo para `ATIVO` ou `ATRASADO`.

### 5.5. Multa

Representa uma penalidade financeira gerada por atraso na devolução de um exemplar.

| Campo | Tipo | Obrigatório | Restrições |
|---|---|---|---|
| id | Integer | Sim | PK |
| usuario_id | Integer | Sim | FK Usuário |
| emprestimo_id | Integer | Sim | FK Empréstimo |
| valor | Decimal | Sim | >= 0 |
| status | Enum | Sim | PENDENTE, PAGA |

Relacionamentos:

Uma multa pertence a um usuário.

Uma multa está vinculada a um único empréstimo.

Cardinalidades:

```text
Multa N:1 Usuario
Multa 1:1 Emprestimo
```

Máquina de estados:

```text
PENDENTE ───────► PAGA
```

O estado `PAGA` é terminal. Após o pagamento, não é permitido retornar a multa para o estado `PENDENTE`.

### 5.6. LogEmprestimo

Entidade planejada para uma migration futura.

Representa o histórico de eventos relevantes ocorridos durante o ciclo de vida de um empréstimo.

| Campo | Tipo | Obrigatório | Restrições |
|---|---|---|---|
| id | Integer | Sim | PK |
| emprestimo_id | Integer | Sim | FK Empréstimo |
| acao | Enum | Sim | Evento |
| data_evento | DateTime | Sim | Obrigatória |

Eventos possíveis:

```text
EMPRESTIMO_CRIADO
ATRASO_IDENTIFICADO
MULTA_GERADA
DEVOLVIDO
MULTA_PAGA
```

Relacionamento:

```text
LogEmprestimo N:1 Emprestimo
```

Essa entidade terá finalidade de auditoria e rastreabilidade.

## 6. Cálculos derivados

### 6.1. Quantidade de exemplares disponíveis

A quantidade de exemplares disponíveis não será armazenada na tabela `livros`.

Fórmula:

```text
COUNT(exemplares WHERE status = 'DISPONIVEL')
```

Justificativa:

Essa decisão evita inconsistências entre um campo de estoque salvo no livro e a situação real dos exemplares.

### 6.2. Valor da multa

O valor da multa será calculado com base nos dias de atraso.

Fórmula:

```text
Valor da Multa = Dias de Atraso × Valor Diário
```

Justificativa:

Essa regra permite aplicar penalidades proporcionais ao atraso na devolução.

## 7. Regras de negócio

### RN-001 - Exemplar deve estar disponível

| **Campo**         | Descrição                                                |
| ----------------- | -------------------------------------------------------- |
| **Identificador** | RN-001                                                   |
| **Nome**          | Exemplar deve estar disponível                           |
| **Gatilho**       | Criação de empréstimo                                    |
| **Pré-condição**  | Exemplar com status `DISPONIVEL`                         |
| **Ação**          | Criar empréstimo e alterar exemplar para `EMPRESTADO`    |
| **Violação**      | HTTP 409 - `EXEMPLAR_UNAVAILABLE`                        |

### RN-002 - Usuário com multa pendente não pode realizar empréstimos

| **Campo**         | Descrição                                                |
| ----------------- | -------------------------------------------------------- |
| **Identificador** | RN-002                                                   |
| **Nome**          | Usuário com multa pendente não pode realizar empréstimos |
| **Gatilho**       | Criação de empréstimo                                    |
| **Pré-condição**  | Não existir multa com status `PENDENTE`                  |
| **Ação**          | Permitir empréstimo                                      |
| **Violação**      | HTTP 403 - `USER_HAS_PENDING_FINE`                       |

### RN-003 - Limite máximo de empréstimos ativos

| **Campo**         | Descrição                                     |
| ----------------- | --------------------------------------------- |
| **Identificador** | RN-003                                        |
| **Nome**          | Limite máximo de empréstimos ativos           |
| **Gatilho**       | Criação de empréstimo                         |
| **Pré-condição**  | Usuário possuir menos de 3 empréstimos ativos |
| **Ação**          | Permitir empréstimo                           |
| **Violação**      | HTTP 403 - `MAX_ACTIVE_LOANS_REACHED`         |

### RN-004 - Atraso gera multa

| **Campo**         | Descrição                                    |
| ----------------- | -------------------------------------------- |
| **Identificador** | RN-004                                       |
| **Nome**          | Atraso gera multa                            |
| **Gatilho**       | Atualização de empréstimos pelo sistema      |
| **Pré-condição**  | Data atual maior que `devolucao_prevista`    |
| **Ação**          | Alterar status para `ATRASADO` e gerar multa |
| **Violação**      | Não aplicável diretamente ao usuário         |

### RN-005 - Não é possível devolver empréstimo finalizado

| **Campo**         | Descrição                                              |
| ----------------- | ------------------------------------------------------ |
| **Identificador** | RN-005                                                 |
| **Nome**          | Não é possível devolver empréstimo finalizado          |
| **Gatilho**       | Registro de devolução                                  |
| **Pré-condição**  | Empréstimo não pode estar `FINALIZADO`                 |
| **Ação**          | Registrar devolução e alterar status para `FINALIZADO` |
| **Violação**      | HTTP 409 - `LOAN_ALREADY_FINISHED`                     |

### RN-006 - Multa paga não pode ser paga novamente

| **Campo**         | Descrição                              |
| ----------------- | -------------------------------------- |
| **Identificador** | RN-006                                 |
| **Nome**          | Multa paga não pode ser paga novamente |
| **Gatilho**       | Pagamento de multa                     |
| **Pré-condição**  | Multa deve possuir status `PENDENTE`   |
| **Ação**          | Alterar status para `PAGA`             |
| **Violação**      | HTTP 409 - `FINE_ALREADY_PAID`         |

### RN-007 - Devolução libera exemplar

| **Campo**         | Descrição                                    |
| ----------------- | -------------------------------------------- |
| **Identificador** | RN-007                                       |
| **Nome**          | Devolução libera exemplar                    |
| **Gatilho**       | Registro de devolução                        |
| **Pré-condição**  | Empréstimo com status `ATIVO` ou `ATRASADO`  |
| **Ação**          | Alterar status do exemplar para `DISPONIVEL` |
| **Violação**      | HTTP 409 - `INVALID_LOAN_STATE`              |

### RN-008 - Eventos relevantes devem ser registrados no histórico de empréstimos

| **Campo**         | Descrição                                             |
| ----------------- | ----------------------------------------------------- |
| **Identificador** | RN-008                                                |
| **Nome**          | Eventos relevantes devem ser registrados no histórico |
| **Gatilho**       | Criação, atraso, devolução ou pagamento de multa      |
| **Pré-condição**  | Existência de um empréstimo associado                 |
| **Ação**          | Registrar evento em `LogEmprestimo`                   |
| **Violação**      | HTTP 500 - `LOAN_HISTORY_REGISTRATION_FAILED`         |

### RN-009 - Valor da multa não pode ser negativo

| **Campo**         | Descrição                            |
| ----------------- | ------------------------------------ |
| **Identificador** | RN-009                               |
| **Nome**          | Valor da multa não pode ser negativo |
| **Gatilho**       | Geração de multa                     |
| **Pré-condição**  | Dias de atraso maior ou igual a zero |
| **Ação**          | Calcular valor da multa              |
| **Violação**      | HTTP 400 - `INVALID_FINE_VALUE`      |

Observação:

Esta regra será implementada junto com a migration futura de auditoria, responsável pela criação da tabela `log_emprestimos`.

## 8. Decisões de design relevantes

Esta seção será aprofundada durante o desenvolvimento e apresentação do projeto.

### 8.1. Por que o empréstimo aponta para Exemplar e não para Livro?

O livro representa a obra bibliográfica. O exemplar representa a cópia física que realmente sai da biblioteca.

Se o empréstimo fosse feito diretamente sobre o livro, o sistema não saberia qual cópia foi emprestada. Por isso, o empréstimo referencia `exemplar_id`.

### 8.2. Por que o estoque não fica salvo na tabela Livro?

O estoque é um valor derivado.

A disponibilidade depende da quantidade de exemplares com status `DISPONIVEL`. Salvar um campo `estoque` em `livros` poderia gerar inconsistência caso o status dos exemplares mudasse e o estoque não fosse atualizado corretamente.

### 8.3. Por que usar status em vez de booleano na multa?

A multa poderia ter um campo booleano, como `paga = true` ou `paga = false`.

Porém, o campo `status` deixa o domínio mais claro e facilita evoluções futuras. Na versão inicial, os estados são `PENDENTE` e `PAGA`.

### 8.4. Por que regras de negócio ficam na camada de service?

Os routers devem apenas receber requisições e chamar os services.

As regras de negócio ficam nos services porque elas dependem do domínio e frequentemente precisam consultar várias entidades. Por exemplo, ao criar um empréstimo, é necessário verificar exemplar, usuário, multas pendentes e limite de empréstimos ativos.

### 8.5. O que fica nos validators do Pydantic?

Os schemas Pydantic serão usados para validar formato e consistência simples dos dados de entrada.

Exemplos:

```text
nome não vazio
email válido
senha obrigatória
data prevista coerente
limit e offset válidos
```

Regras que dependem de consulta ao banco ficam na camada de service.

### 8.6. Por que a migration de log será separada?

A tabela `log_emprestimos` representa uma evolução do domínio para auditoria.

Separá-la em uma migration própria ajuda a contar a história de evolução do banco, em vez de criar tudo em uma única migration.

### 8.7. Como tratar dois usuários tentando emprestar o mesmo exemplar?

A criação do empréstimo deve acontecer em transação.

O sistema precisa verificar o status atual do exemplar e alterar o status para `EMPRESTADO` dentro da mesma operação. Em uma versão mais robusta, pode ser usado bloqueio de linha no banco para evitar condição de corrida.

### 8.8. Quais estados são terminais?

No empréstimo, `FINALIZADO` é terminal.

Na multa, `PAGA` é terminal.

Esses estados são terminais porque, depois da devolução de um empréstimo ou do pagamento de uma multa, não faz sentido retornar ao estado anterior sem criar inconsistência no histórico do sistema.

## 9. Cenários de borda

### 9.1. Excluir usuário com empréstimos ativos

Decisão:

Não permitir exclusão de usuário com empréstimos ativos.

Justificativa:

Excluir um usuário com empréstimos em andamento prejudicaria o histórico e a consistência do sistema.

### 9.2. Excluir livro com exemplares cadastrados

Decisão:

Não permitir exclusão direta de livro que possui exemplares cadastrados.

Justificativa:

O livro é entidade pai dos exemplares. Remover o livro sem tratar os exemplares poderia gerar perda de histórico ou registros inconsistentes.

### 9.3. Criar empréstimo sem exemplar disponível

Decisão:

Bloquear a criação do empréstimo.

Justificativa:

O recurso físico limitado do sistema é o exemplar. Se não houver exemplar disponível, o empréstimo não pode ocorrer.

### 9.4. Devolver empréstimo finalizado

Decisão:

Bloquear a operação.

Justificativa:

`FINALIZADO` é um estado terminal.

### 9.5. Pagar multa já paga

Decisão:

Bloquear a operação.

Justificativa:

`PAGA` é um estado terminal.

### 9.6. Cálculo de multa negativo

Decisão:

Bloquear valor negativo.

Justificativa:

A multa é uma penalidade por atraso. Se o cálculo resultar em valor negativo, existe erro de data ou regra.

## 10. Catálogo de erros

Esta seção será preenchida durante a implementação das exceções e handlers globais da API.

Os erros de negócio seguirão o formato abaixo:

```json
{
  "error": "CODIGO_DO_ERRO",
  "message": "Mensagem legível para o usuário.",
  "details": {
    "campo": "valor contextual"
  }
}
```

Erros planejados:

```text
EXEMPLAR_UNAVAILABLE
USER_HAS_PENDING_FINE
MAX_ACTIVE_LOANS_REACHED
LOAN_ALREADY_FINISHED
FINE_ALREADY_PAID
INVALID_LOAN_STATE
LOAN_HISTORY_REGISTRATION_FAILED
INVALID_FINE_VALUE
```

## 11. Migrations planejadas

O projeto usará Alembic para versionamento do banco de dados.

### Migration 1 - Estrutura inicial

Criação das tabelas principais:

```text
usuarios
livros
exemplares
emprestimos
multas
```

### Migration 2 - Índices, constraints ou evolução de regra

Possíveis alterações:

```text
índice para multas por usuario_id e status
índice para emprestimos por usuario_id e status
constraint UNIQUE em multas.emprestimo_id
campo perfil em usuarios, se houver controle administrativo
```

Justificativa:

Essa migration representa uma evolução do entendimento das regras de negócio e das consultas necessárias para aplicar essas regras.

### Migration 3 - Auditoria

Criação da tabela:

```text
log_emprestimos
```

Justificativa:

A tabela de logs registra eventos relevantes do ciclo de vida do empréstimo, permitindo auditoria e rastreabilidade.

## 12. Teste de rollback das migrations

Cada migration deve possuir `upgrade` e `downgrade`.

Comandos planejados:

```bash
alembic upgrade head
alembic current
alembic downgrade -1
alembic current
alembic upgrade head
alembic downgrade base
alembic upgrade head
```

Resultado esperado:

`alembic upgrade head` aplica todas as migrations.

`alembic downgrade -1` desfaz apenas a última migration.

`alembic downgrade base` remove todas as alterações aplicadas pelas migrations.

Após executar novamente `alembic upgrade head`, o banco volta para a versão mais recente sem erros.

## 13. Endpoints planejados

### Usuários

```text
POST /usuarios
GET /usuarios?limit=10&offset=0
```

### Livros

```text
POST /livros
GET /livros?titulo=&autor=&limit=10&offset=0
GET /livros/{livro_id}/disponibilidade
```

### Exemplares

```text
POST /livros/{livro_id}/exemplares
GET /exemplares?livro_id=&status=
```

### Empréstimos

```text
POST /emprestimos
GET /emprestimos?usuario_id=&status=&limit=10&offset=0
PATCH /emprestimos/{emprestimo_id}/devolver
POST /emprestimos/atualizar-atrasos
```

### Multas

```text
GET /multas?usuario_id=&status=
PATCH /multas/{multa_id}/pagar
```

### Logs

Endpoints planejados para depois da migration de auditoria:

```text
GET /emprestimos/{emprestimo_id}/logs
```

## 14. Testes automatizados

O projeto usará pytest.

Comando planejado para rodar os testes dentro do container:

```bash
docker compose run api pytest
```

Cenários principais:

```text
criar empréstimo com exemplar disponível
bloquear empréstimo com exemplar indisponível
bloquear empréstimo para usuário com multa pendente
bloquear empréstimo quando usuário possui 3 empréstimos ativos
devolver empréstimo ativo
bloquear devolução de empréstimo finalizado
verificar se devolução libera exemplar
atualizar empréstimo atrasado
gerar multa para empréstimo atrasado
pagar multa pendente
bloquear pagamento de multa já paga
calcular disponibilidade de livro pelos exemplares
```

## 15. Regras futuras

As regras abaixo foram identificadas durante a modelagem, mas não fazem parte da implementação inicial.

### RN-F01 - Reserva de livro somente quando não houver exemplares disponíveis

Um usuário só poderá reservar um livro caso não exista exemplar disponível no momento da solicitação.

### RN-F02 - Usuário não pode possuir duas reservas ativas para o mesmo livro

Evita duplicidade de reservas para o mesmo usuário e livro.

### RN-F03 - Ao devolver um exemplar reservado, o próximo usuário da fila deve ser notificado

Permite evolução do sistema para uma fila de espera de reservas.

## 16. Possível implementação futura de reservas

A entidade `Reserva` poderá ser adicionada futuramente.

Campos planejados:

| Campo | Tipo | Obrigatório | Restrições |
|---|---|---|---|
| id | Integer | Sim | PK |
| usuario_id | Integer | Sim | FK Usuário |
| livro_id | Integer | Sim | FK Livro |
| status | Enum | Sim | ATIVA, DISPONIVEL, CANCELADA |
| data_reserva | DateTime | Sim | Obrigatória |

A reserva será vinculada ao livro, e não ao exemplar, pois o usuário reserva a obra desejada. O exemplar específico será definido apenas quando houver uma cópia disponível.

## 17. Considerações finais


Este projeto foi planejado para demonstrar domínio sobre modelagem, regras de negócio, estados de ciclo de vida, migrations, validações e consistência de dados.

A separação entre livro e exemplar permite controlar corretamente os recursos físicos da biblioteca. O cálculo de disponibilidade evita inconsistências de estoque. A separação em camadas facilita manutenção e testes. As migrations incrementais ajudam a demonstrar a evolução do banco durante o desenvolvimento.
