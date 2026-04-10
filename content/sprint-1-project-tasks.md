# FastInBox - Sprint 1 Tasks (Project Format)

## Cards para o Project da Organizacao

| Title | Status | Sprint | Priority | Tipo | Descricao | Criterios de aceite |
| --- | --- | --- | --- | --- | --- | --- |
| S1 - Autenticacao por perfil (nutri, paciente, fabrica) | In Progress | Sprint 1 | Alta | Feature | Implementar login e cadastro por perfil com persistencia local para demo. | Usuario consegue cadastrar e entrar por perfil correto; sessao ativa e logout funcionando. |
| S1 - Cadastro de pacientes pelo nutricionista | In Progress | Sprint 1 | Alta | Feature | Permitir que o nutricionista cadastre pacientes no painel e reutilize no pedido. | Novo paciente aparece na lista imediatamente e pode ser selecionado no fluxo de pedido. |
| S1 - Criacao de marmita vinculada ao paciente | In Progress | Sprint 1 | Alta | Feature | Criar fluxo de novo pedido com itens, ingredientes, preco e vinculacao ao paciente. | Pedido gerado com codigo unico e dados completos de itens/valores/paciente. |
| S1 - Envio de pedido para fabrica | In Progress | Sprint 1 | Alta | Feature | No fechamento do pedido, selecionar fabrica responsavel e encaminhar para fila operacional. | Pedido aparece no kanban da fabrica selecionada com status inicial de producao. |
| S1 - Dashboard do nutricionista com acompanhamento | In Progress | Sprint 1 | Media | Feature | Mostrar metricas e pedidos recentes do nutricionista em cards. | Dashboard exibe status atualizados dos pedidos e acesso aos detalhes. |
| S1 - Dashboard do paciente com andamento em cards | In Progress | Sprint 1 | Media | Feature | Exibir pedidos do paciente logado em cards com status e acesso rapido ao rastreio. | Paciente visualiza andamento e abre timeline de status por pedido. |
| S1 - Kanban da fabrica com drag-and-drop | In Progress | Sprint 1 | Alta | Feature | Painel da fabrica com colunas de status e movimentacao por arrastar e soltar. | Pedido muda de coluna e status persiste apos refresh. |
| S1 - Pagamento e atualizacao de status | In Progress | Sprint 1 | Media | Feature | Fluxo de pagamento simples para pedidos pendentes com atualizacao para status pago. | Ao concluir pagamento, pedido atualiza e entra no fluxo de producao. |
| S1 - Estrategia de entrega da Sprint 1 | In Progress | Sprint 1 | Alta | Infra | Consolidar MVP com fluxo principal funcional e baixa complexidade operacional. | Aplicacao em producao com jornada principal estavel e documentacao atualizada. |
| S1 - Revisao final para apresentacao academica | In Progress | Sprint 1 | Media | QA | Revisar rotas, estados, feedbacks e consistencia visual da jornada ponta a ponta. | Navegacao sem quebras e experiencia coerente em desktop/mobile. |

## Campos sugeridos no GitHub Projects

- `Status`: In Progress
- `Sprint`: Sprint 1
- `Priority`: Alta/Media
- `Tipo`: Feature/Infra/QA
- `Owner`: definir por card
