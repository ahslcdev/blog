# Blog .novadata

## Este arquivo serve para explicar sobre a aplicação desenvolvida

## Sumário
1. Sobre o projeto
2. Tecnologias
3. Considerações iniciais
4. Funcionalidades implementadas
5. Testes

## Sobre o projeto
- Desenvolver uma aplicação que permita a criação de postagems e comentários para estas postagens.
- Otimizar as consultas SQL

## Tecnologias
- PostgreSQL
- Redis
- Django 4.2
- Django Rest framework 3.14

## Considerações iniciais
- A aplicação possui 2 endpoints para login e logout, isso se deve ao fato de que foram utilizadas SESSION e JWT para view e viewsets respectivamente.
- A API possui funcionalidades que não estão disponíveis em tela apenas através do Swagger ou então de consumo pelo Insomnia ou Postman

## Funcionalidades implementas
### Solicitadas
- CRUD de Postagens (Via API, Admin e Views)
- CRUD de Comentários (Via API, Admin e Views)
- CRUD de Usuários (Via API, Admin e View (Somente CREATE))
- Login e Logout

### Fora do escopo
- Filtros adicionados no endpoint GET de postagens. endpoint: /api/posts/?=
- - Filtros disponíveis: search, data_inicial, data_final

### Testes
- Foi utilizado o Swagger da OPENAI para gerar documentação para a API do projeto. Através deste swagger é possível realizar todas as operações de CRUD, bem como acessar os endpoints de autenticação. endpoint: /swagger
- O swagger explica como deve ser as solicitações HTTP, quais campos devem ser mandados.
- Além do swagger, foram realizados teste unitários no qual foram testados todos os endpoints e possíveis situações que possam acontecer durante o uso da aplicação.
- Para rodar os testes basta rodar o comando 'python manage.py test tests'
- A função de teste que testa o CACHE foi nomeada como 'test_post_list_success_cache' e está no arquivo /tests/tests_api.py, devido a implementação desta função os testes demoram um pouco devido a um SLEEP que foi utilizado no código para testar efetivamente.


