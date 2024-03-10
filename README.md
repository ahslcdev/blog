# Blog .novadata

## Este arquivo serve para explicar sobre a aplicação desenvolvida

## Sumário
1. Sobre o projeto
2. Considerações iniciais
3. Funcionalidades implementadas
4. Testes


## Sobre o projeto
- Desenvolver uma aplicação que permita a criação de postagems e comentários para estas postagens.
- Otimizar as consultas SQL

## Considerações iniciais
- A aplicação possui 2 endpoints para login e logout, isso se deve ao fato de que foram utilizadas SESSION e JWT para view e viewsets respectivamente.

## Funcionalidades implementas
### Solicitadas
- CRUD de Postagens
- CRUD de Comentários
- Login e Logout

### Fora do escopo
- Filtros adicionados no endpoint GET de postagens. endpoint: /api/posts/?=
- - Filtros disponíveis: search, data_inicial, data_final

### Testes
- Foi utilizado o Swagger da OPENAI para gerar documentação para a API do projeto. Através deste swagger é possível realizar todas as operações de CRUD, bem como acessar os endpoints de autenticação. endpoint: /swagger
- O swagger explica como deve ser as solicitações HTTP, quais campos devem ser mandados.
- Além do swagger, foram realizados teste unitários no qual foram testados todos os endpoints e possíveis situações que possam acontecer durante o uso da aplicação.
- Para rodar os testes basta rodar o comando 'python manage.py test tests'


