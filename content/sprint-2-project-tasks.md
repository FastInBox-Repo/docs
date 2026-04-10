# FastInBox - Sprint 2 Tasks (Project Format)

## Cards para o Project da Organizacao

| Title | Status | Sprint | Priority | Tipo | Descricao | Criterios de aceite |
| --- | --- | --- | --- | --- | --- | --- |
| S2 - Integrar autenticacao e sessao com API real | Todo | Sprint 2 | Alta | Feature | Conectar login, sessao e validacao de perfil do front aos endpoints reais do backend. | Usuario consegue autenticar sem depender apenas do estado local e a sessao respeita o perfil selecionado. |
| S2 - Persistir pacientes do nutricionista no servidor | Todo | Sprint 2 | Alta | Feature | Implementar persistencia e listagem de pacientes vinculados ao nutricionista autenticado. | Paciente criado reaparece apos refresh e fica associado ao nutricionista correto. |
| S2 - Persistir pedidos e fabrica responsavel em banco | Todo | Sprint 2 | Alta | Feature | Salvar pedido, itens, paciente e fabrica responsavel em base relacional para consulta pelos perfis. | Pedido pode ser recuperado nos paineis do nutricionista, paciente e fabrica com o mesmo codigo. |
| S2 - Sincronizar kanban da fabrica com status server-side | Todo | Sprint 2 | Alta | Feature | Atualizar leitura e mudanca de status da cozinha usando dados reais do backend. | Mudanca de coluna permanece apos refresh e aparece corretamente em outras telas. |
| S2 - Instrumentar eventos criticos de pagamento e status | Todo | Sprint 2 | Media | Feature | Registrar eventos minimos do fluxo critico para auditoria e leitura operacional. | Existe historico rastreavel para pagamento, confirmacao e avancos de etapa. |
| S2 - Criar smoke test da jornada E2E principal | Todo | Sprint 2 | Alta | QA | Automatizar o fluxo principal de criar pedido, pagar e acompanhar status. | Teste executa com sucesso no baseline da sprint e acusa regressao quando o fluxo quebra. |
| S2 - Refinar feedbacks visuais da jornada do paciente | Todo | Sprint 2 | Media | UX | Melhorar mensagens de carregamento, sucesso, erro e acompanhamento do pedido no front. | Paciente entende com clareza o estado atual e o proximo passo em cada tela critica. |
| S2 - Consolidar evidencias e documentos da sprint | Todo | Sprint 2 | Media | Docs | Atualizar review, backlog e evidencias publicas da sprint para banca e continuidade do projeto. | Pages reflete o andamento real da sprint e os artefatos estao centralizados. |

## Campos sugeridos no GitHub Projects

- `Status`: Todo
- `Sprint`: Sprint 2
- `Priority`: Alta/Media
- `Tipo`: Feature/QA/UX/Docs
- `Owner`: definir conforme disponibilidade da equipe
