# FastInBox - Sprint 3 Tasks (Project Format)

## Objetivo da Sprint #03

Migrar o fluxo principal do MVP (nutricionista -> paciente -> cozinha) da persistencia local para uma base server-side, com API real, autenticacao/autorizacao por perfil e sincronizacao de status entre telas.

## Cards para o Project da Organizacao

| Title | Status | Sprint | Priority | Tipo | Responsavel | Descricao (o que) | Como fazer (detalhamento) | Criterios de aceite |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S3 - Provisionar banco PostgreSQL e ambiente base | Todo | Sprint 3 | Alta | Infra | Joao Vitor | Criar ambiente de dados para o backend real. | Subir PostgreSQL (dev/hml), validar conexao no backend e registrar variaveis no `.env.example`. | API conecta no banco sem erro; script/documentacao de setup validado pela equipe. |
| S3 - Estruturar modulos de dominio no backend | Todo | Sprint 3 | Alta | Back | Thiago | Organizar backend por modulos (auth, pacientes, pedidos, status). | Criar pastas, services e controllers iniciais com contratos tipados e tratamento basico de erro. | Estrutura modular funcionando com build sem erros e rotas registradas. |
| S3 - Persistir pacientes no servidor | Todo | Sprint 3 | Alta | Back | Thiago | Tirar cadastro de paciente do store local como fonte principal. | Criar endpoints CRUD de pacientes vinculados ao nutricionista autenticado. | Criar/listar pacientes via API; dado persiste apos reinicio do front. |
| S3 - Persistir pedidos e fabrica responsavel em banco | In Review | Sprint 3 | Alta | Back | Thiago | Salvar pedido, itens e fabrica em banco relacional. | Criar entidades de pedido/item/fabrica + endpoint de criacao e consulta por perfis. | Pedido criado reaparece em nutricionista, paciente e cozinha usando API real. |
| S3 - Implementar autenticacao server-side por perfil | Todo | Sprint 3 | Alta | Back | Thiago | Substituir login local por autenticacao real. | Criar login com token/sessao e middleware/guard por perfil. | Usuario autentica por perfil e recebe apenas escopo permitido nas rotas. |
| S3 - Integrar front ao backend (pacientes e pedidos) | Todo | Sprint 3 | Alta | Front | Thiago | Conectar telas principais ao backend. | Implementar camada de chamadas de API e remover dependencia direta do `localStorage` para fluxos principais. | Front cria/lista pacientes e pedidos via API sem quebra de navegacao. |
| S3 - Sincronizar kanban da cozinha com dados do servidor | Todo | Sprint 3 | Alta | Front | Thiago | Fazer status da cozinha ser fonte unica no servidor. | Atualizar dashboard/cozinha para consumir e atualizar status via endpoint. | Mudanca de status persiste apos refresh e aparece no status do paciente. |
| S3 - Cobrir fluxo nutricionista -> paciente (ate confirmacao) | In Review | Sprint 3 | Media | QA | Gabriel | Validar jornada principal da Sprint 3. | Rodar roteiro de teste funcional com evidencias e validar regressao nas telas chave. | Fluxo testado ponta a ponta com evidencias e sem erros bloqueantes. |
| S3 - Atualizar documentacao tecnica da Sprint 3 | Todo | Sprint 3 | Media | Docs | Joao Vitor | Publicar backlog, progresso e evidencias de forma coerente. | Atualizar documentos de sprint com links de tasks, status e pendencias reais. | Documentacao alinhada ao board e ao estado real do codigo. |

## Alocacao dos Integrantes (quem vai fazer)

- **Thiago:** Back-end e integracao front/back dos fluxos centrais.
- **Joao Vitor:** Infra/ambiente (banco, variaveis, setup) e suporte na documentacao tecnica.
- **Gabriel:** QA funcional da jornada principal e apoio de validacao da experiencia.

## Definition of Done da Sprint #03

- Fluxo principal deixa de depender apenas de persistencia local para pacientes/pedidos/status.
- API real responde para os endpoints centrais da jornada.
- Regras de acesso por perfil estao minimamente aplicadas.
- Backlog atualizado no Project com status real (Todo / In Progress / In Review / Done).
- Evidencias de validacao registradas para os itens criticos.

## Entregavel da Aula (Sprint Backlog #03)

Para atender ao pedido da disciplina, apresentar:

1. **Objetivo da sprint** (1 paragrafo curto).
2. **Itens da sprint com detalhamento de execucao** (tabela acima).
3. **Alocacao de integrantes por frente**.
4. **Criterios de aceite por item**.
5. **Status atual no Project** (o que esta em review, em progresso e pendente).

