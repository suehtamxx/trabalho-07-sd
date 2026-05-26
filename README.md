# Projeto de Avaliação de Desempenho

Este projeto compara duas implementações de uma API FastAPI para demonstrar a diferença de desempenho entre uma versão baseline e uma versão otimizada.

## Objetivo

Comparar o comportamento de uma API monolítica em duas versões:
- `main.py`: implementação baseline com problema de N+1 queries
- `main_otimizado.py`: implementação otimizada usando relacionamento e `joinedload`

O foco é mostrar como pequenas mudanças na camada de acesso ao banco podem impactar o desempenho sob carga.

## Estrutura do projeto

- `main.py` - API baseline com consultas ineficientes ao banco
- `main_otimizado.py` - API otimizada usando join antecipado de relacionamentos
- `locustfile.py` - definição de carga para Locust
- `rodar_testes.py` - script que executa 5 rodadas de teste com Locust e salva resultados em CSV
- `results/` - pasta de saída dos relatórios de carga
- `teste_carga.db` - banco SQLite gerado automaticamente

## Tecnologias usadas

- Python 3
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- Locust

## Como usar

### 1. Preparar ambiente

Recomenda-se usar um ambiente virtual:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install fastapi uvicorn sqlalchemy pydantic locust
```

### 2. Executar a API

#### Baseline

```powershell
uvicorn main:app --reload
```

#### Otimizada

```powershell
uvicorn main_otimizado:app --reload
```

Ambas as APIs utilizam o mesmo banco SQLite `teste_carga.db` e preenchem dados de teste automaticamente no primeiro acesso.

### 3. Executar teste de carga

Com a API rodando em `http://localhost:8000`, execute:

```powershell
python rodar_testes.py
```

O script executa 5 rodadas de Locust com as seguintes configurações:
- 50 usuários simultâneos
- 10 usuários adicionados por segundo
- 5 minutos de duração total por rodada
- 1 minuto de warm-up descartado (implementado no `locustfile.py`)

Os resultados são salvos em `results/`.

## Endpoints

- `GET /api/recurso-lento`
  - Retorna todos os clientes com total de pedidos
  - Versão baseline faz uma consulta de pedidos para cada cliente
  - Versão otimizada usa `joinedload` para carregar relacionamentos em uma única consulta

- `GET /api/recurso-detalhe/{id}`
  - Retorna o cliente pelo ID

- `GET /api/status`
  - Healthcheck simples

- `POST /api/recurso`
  - Cria um novo cliente
  - Exemplo de payload: `{ "nome": "Cliente X" }`

## Observações

- A pasta `results/` é criada automaticamente pelo `rodar_testes.py`
- Caso precise limpar os resultados, remova os arquivos CSV dentro de `results/`
- O arquivo SQLite `teste_carga.db` é reutilizado entre execuções e fica no diretório do projeto

