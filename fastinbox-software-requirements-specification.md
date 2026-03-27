# FastInBox - Especificacao de Requisitos de Software (ERS)

**Classificacao:** Confidencial  
**Distribuicao:** Uso interno autorizado  
**Status do documento:** Draft para validacao  
**Versao:** 1.0  
**Data:** 2026-03-20  

## Aviso de confidencialidade

Este documento contem informacoes estrategicas, funcionais e operacionais da plataforma FastInBox. Sua reproducao, compartilhamento ou divulgacao parcial ou integral depende de autorizacao previa dos responsaveis pelo produto.

## 1. Controle do documento

| Campo | Valor |
| --- | --- |
| Produto | FastInBox |
| Tipo de documento | Especificacao de Requisitos de Software |
| Objetivo | Consolidar os requisitos de negocio, funcionais e nao funcionais da plataforma |
| Publico-alvo | Produto, design, front-end, back-end, QA, operacoes e stakeholders executivos |
| Origem das informacoes | Documento base de requisitos e estruturacao da ideia do produto |

### 1.1 Responsaveis

| Area | Responsavel |
| --- | --- |
| Produto | A definir |
| Front-end | A definir |
| Back-end | A definir |
| Design | A definir |
| Operacoes | A definir |

### 1.2 Historico de versoes

| Versao | Data | Autor | Descricao |
| --- | --- | --- | --- |
| 1.0 | 2026-03-20 | Thiago | Consolidacao inicial dos requisitos em formato enterprise |

## 2. Visao executiva

O FastInBox e uma plataforma digital para operacao white label de marmitas personalizadas, conectando nutricionistas, pacientes, cozinhas parceiras e administradores em um unico fluxo operacional. O sistema deve permitir a criacao, revisao, pagamento, producao, entrega e acompanhamento de pedidos personalizados, preservando a identidade visual da clinica do nutricionista e garantindo governanca sobre comissoes, status operacionais e experiencia do usuario.

## 3. Objetivos do produto

- centralizar o fluxo ponta a ponta entre clinica, paciente, cozinha e administracao
- permitir a revenda white label de marmitas personalizadas por nutricionistas
- reduzir operacao manual na montagem, confirmacao e entrega dos pedidos
- oferecer experiencia clara e responsiva em desktop, tablet e mobile
- manter rastreabilidade operacional, financeira e administrativa

## 4. Escopo

### 4.1 Escopo em foco

- autenticacao e gestao de acesso por perfil
- jornada do nutricionista para cadastro de pacientes e criacao de pedidos
- jornada do paciente para acesso, revisao, confirmacao, pagamento e acompanhamento
- painel operacional da cozinha para producao e entrega
- painel administrativo para gestao de usuarios, pedidos, comissoes e regras
- suporte a white label da clinica
- base para planos recorrentes, previsao de demanda e conciliacao financeira

### 4.2 Fora de escopo detalhado neste documento

Os itens abaixo podem existir futuramente, mas nao possuem detalhamento suficiente nesta versao:

- aplicativo mobile nativo
- integracoes fiscais ou ERP
- roteirizacao logistica avancada
- regras tributarias por municipio ou estado
- automacoes de marketing e CRM

## 5. Contexto de negocio

### 5.1 Modelo operacional

1. O nutricionista cadastra o paciente ou inicia um pedido associado a ele.
2. O nutricionista monta um ou mais itens de marmita, define embalagem e comissao.
3. O sistema gera um codigo unico de pedido para compartilhamento.
4. O paciente acessa o pedido via codigo, revisa os dados, faz ajustes permitidos e confirma.
5. O paciente realiza o pagamento sem redirecionamento externo.
6. O pedido pago e disponibilizado para a cozinha parceira.
7. A cozinha produz, atualiza status e organiza a entrega em janelas pre-definidas.
8. A administracao monitora operacao, usuarios, regras, relatorios e indicadores.

### 5.2 Diferenciais de negocio

- operacao white label com prioridade visual para a marca da clinica
- personalizacao do pedido por paciente
- comissionamento progressivo para nutricionistas
- consolidacao operacional entre venda, producao e entrega

## 6. Stakeholders e perfis de acesso

| Perfil | Descricao | Objetivo principal |
| --- | --- | --- |
| Nutricionista | Profissional ou clinica parceira | Cadastrar pacientes, montar pedidos, configurar marca e acompanhar status |
| Paciente | Cliente final da refeicao | Revisar, editar quando permitido, pagar e acompanhar o pedido |
| Cozinha | Parceiro operacional de producao e entrega | Receber pedidos pagos, produzir, atualizar status e planejar entregas |
| Administrador | Time interno do FastInBox | Gerir usuarios, operacao, regras, relatorios e parceiros |

## 7. Premissas e dependencias

- a plataforma sera web, responsiva e acessivel em navegadores modernos
- a camada de front-end sera implementada em TypeScript com React ou Next.js
- a camada de back-end sera implementada em Node.js com NestJS
- o armazenamento principal sera PostgreSQL ou banco relacional equivalente
- o pagamento exigira integracao com gateway compativel com checkout integrado
- operacoes sensiveis deverao ser auditaveis

## 8. Diretrizes de negocio e operacao

### 8.1 Principios obrigatorios

- a experiencia do paciente deve priorizar a marca da clinica e nao a marca operacional da FastInBox
- nenhum pedido deve seguir para a cozinha sem confirmacao e pagamento aprovados
- toda alteracao de status relevante deve ser registrada de forma rastreavel
- a visibilidade de dados e acoes deve respeitar o perfil de acesso do usuario
- toda regra operacional deve preservar seguranca, privacidade e integridade dos dados

### 8.2 Glossario

| Termo | Definicao |
| --- | --- |
| White label | Operacao em que a marca visivel ao paciente e a da clinica ou nutricionista |
| Pedido | Agrupamento de uma ou mais marmitas, dados do paciente, valores, status e entrega |
| Codigo do pedido | Identificador unico usado pelo paciente para acessar o pedido |
| Comissao | Diferenca entre valor base e valor final praticado pelo nutricionista |
| Janela de entrega | Dia ou periodo definido para consolidacao e expedicao dos pedidos |
| Assinatura | Plano recorrente de pedidos com periodicidade configuravel |

## 9. Requisitos funcionais

### 9.1 Modulo Nutricionista

#### RF-001 - Autenticacao do nutricionista

- **Descricao:** permitir login por e-mail e senha, com mecanismo de recuperacao de senha.
- **Atores:** nutricionista.
- **Entradas / pre-condicoes:** credenciais previamente cadastradas.
- **Fluxo esperado:** o usuario informa credenciais validas, o sistema autentica e libera acesso ao dashboard do perfil.
- **Saidas / pos-condicoes:** acesso autenticado ou mensagem clara de erro em caso de falha.
- **Regras relacionadas:** RNB-005, RNB-007.
- **Criterios minimos de aceite:**
  - login deve validar credenciais antes de abrir a area restrita
  - falhas de autenticacao devem gerar retorno claro sem expor informacoes sensiveis
  - recuperacao de senha deve iniciar fluxo seguro para redefinicao

#### RF-002 - Cadastro e gerenciamento de pacientes

- **Descricao:** permitir o cadastro e a edicao de pacientes vinculados ao nutricionista.
- **Atores:** nutricionista.
- **Entradas / pre-condicoes:** formulario com nome, CPF, e-mail, telefone, endereco e demais campos obrigatorios.
- **Fluxo esperado:** o nutricionista registra ou atualiza os dados do paciente dentro de sua carteira.
- **Saidas / pos-condicoes:** paciente salvo e associado ao nutricionista autenticado.
- **Regras relacionadas:** RNB-005, RNB-007.
- **Criterios minimos de aceite:**
  - o sistema deve validar campos obrigatorios e formatos essenciais
  - o nutricionista deve visualizar pacientes previamente cadastrados
  - a edicao nao deve perder historico relacional com pedidos existentes

#### RF-003 - Criacao de pedido de marmitas

- **Descricao:** permitir que o nutricionista monte pedidos com uma ou mais marmitas, ingredientes, embalagem e comissao, com geracao de codigo unico.
- **Atores:** nutricionista.
- **Entradas / pre-condicoes:** paciente cadastrado e dados do pedido informados.
- **Fluxo esperado:** o nutricionista define a composicao do pedido, configura o valor e gera o pedido.
- **Saidas / pos-condicoes:** pedido criado com codigo unico compartilhavel.
- **Regras relacionadas:** RNB-001, RNB-002, RNB-003.
- **Criterios minimos de aceite:**
  - o pedido deve aceitar multiplas marmitas por solicitacao
  - a comissao deve ser derivada do valor base e do valor final configurado
  - o codigo do pedido deve ser unico e reutilizavel para acesso do paciente

#### RF-004 - Configuracao do perfil da clinica

- **Descricao:** permitir personalizacao da marca da clinica com logotipo e identidade visual.
- **Atores:** nutricionista.
- **Entradas / pre-condicoes:** envio de arquivos e definicao de parametros visuais.
- **Fluxo esperado:** o nutricionista atualiza configuracoes da clinica para refletir a operacao white label.
- **Saidas / pos-condicoes:** perfil da clinica atualizado e aplicado nas interfaces e materiais relacionados.
- **Regras relacionadas:** RNB-001.
- **Criterios minimos de aceite:**
  - o sistema deve aceitar upload de logotipo
  - as configuracoes visuais devem refletir nas telas do paciente quando aplicavel
  - a identidade FastInBox deve permanecer em segundo plano na experiencia white label

#### RF-015 - Gestao de planos recorrentes

- **Descricao:** permitir criacao e manutencao de planos de assinatura com periodicidade semanal, quinzenal ou mensal.
- **Atores:** nutricionista.
- **Entradas / pre-condicoes:** configuracao de frequencia, vigencia, pausas e renovacoes.
- **Fluxo esperado:** o nutricionista define um plano recorrente e o sistema programa a geracao automatica dos pedidos.
- **Saidas / pos-condicoes:** agenda recorrente registrada com pedidos gerados conforme configuracao.
- **Regras relacionadas:** RNB-004, RNB-007.
- **Criterios minimos de aceite:**
  - o plano deve permitir frequencias configuraveis
  - pausas e renovacoes devem impactar apenas os ciclos futuros elegiveis
  - pedidos futuros devem respeitar as regras de entrega vigentes

### 9.2 Modulo Paciente / Cliente Final

#### RF-005 - Acesso ao pedido via codigo

- **Descricao:** permitir que o paciente acesse o pedido por meio do codigo unico informado pelo nutricionista.
- **Atores:** paciente.
- **Entradas / pre-condicoes:** codigo valido informado na landing page de paciente.
- **Fluxo esperado:** o paciente informa o codigo e visualiza os detalhes completos do pedido.
- **Saidas / pos-condicoes:** tela de revisao do pedido carregada com dados validos.
- **Regras relacionadas:** RNB-001, RNB-007.
- **Criterios minimos de aceite:**
  - codigos invalidos devem retornar erro claro
  - o pedido deve carregar dados de itens, nutricionista e clinica
  - o acesso deve respeitar o contexto do pedido associado

#### RF-006 - Edicao e confirmacao do pedido

- **Descricao:** permitir visualizacao, edicao controlada e confirmacao do pedido antes do pagamento.
- **Atores:** paciente.
- **Entradas / pre-condicoes:** pedido carregado a partir de codigo valido.
- **Fluxo esperado:** o paciente revisa ingredientes, informacoes nutricionais e dados pessoais, faz ajustes permitidos e confirma o pedido.
- **Saidas / pos-condicoes:** pedido passa ao estado aguardando pagamento.
- **Regras relacionadas:** RNB-002.
- **Criterios minimos de aceite:**
  - a edicao deve ser bloqueada apos a confirmacao final
  - o sistema deve exigir validacao explicita das informacoes antes do pagamento
  - o status do pedido deve refletir a etapa atual

#### RF-007 - Pagamento do pedido

- **Descricao:** integrar checkout seguro e nativo para pagamento do pedido.
- **Atores:** paciente.
- **Entradas / pre-condicoes:** pedido confirmado e dados de pagamento informados.
- **Fluxo esperado:** o paciente conclui o pagamento dentro da plataforma, sem redirecionamento externo.
- **Saidas / pos-condicoes:** pagamento aprovado atualiza o status do pedido para pago e libera o pedido para a cozinha.
- **Regras relacionadas:** RNB-002, RNB-005, RNB-006.
- **Criterios minimos de aceite:**
  - o fluxo deve suportar meios de pagamento definidos pelo gateway
  - o sistema deve registrar status do pagamento e pedido
  - apenas pagamentos aprovados devem encaminhar o pedido para producao

#### RF-008 - Perfil do paciente

- **Descricao:** disponibilizar area para dados pessoais, historico e acompanhamento de pedidos.
- **Atores:** paciente.
- **Entradas / pre-condicoes:** autenticacao ou acesso associado a pedido valido.
- **Fluxo esperado:** o paciente consulta seu historico, status atuais e dados cadastrais.
- **Saidas / pos-condicoes:** dados exibidos e, quando permitido, atualizados.
- **Regras relacionadas:** RNB-005, RNB-007.
- **Criterios minimos de aceite:**
  - o historico deve listar pedidos anteriores vinculados ao paciente
  - o status de producao e entrega deve ser visivel
  - alteracoes cadastrais devem respeitar politicas de permissao e validacao

#### RF-009 - Autoatendimento para montar pedido

- **Descricao:** permitir que o paciente monte o proprio pedido e informe o codigo do nutricionista para associacao de comissao e marca.
- **Atores:** paciente.
- **Entradas / pre-condicoes:** interface de montagem disponivel e codigo de nutricionista quando aplicavel.
- **Fluxo esperado:** o paciente configura o pedido diretamente e, ao informar o codigo do nutricionista, aplica a vinculacao comercial e visual correspondente.
- **Saidas / pos-condicoes:** pedido criado com associacao correta ao nutricionista informado.
- **Regras relacionadas:** RNB-001, RNB-003, RNB-007.
- **Criterios minimos de aceite:**
  - o sistema deve aceitar montagem direta sem intermedio manual do nutricionista
  - o codigo do nutricionista deve vincular comissao e dados de marca
  - a jornada deve seguir para confirmacao e pagamento como no fluxo padrao

#### RF-016 - Gestao de assinaturas

- **Descricao:** permitir que pacientes modifiquem ou cancelem assinaturas respeitando regras de antecedencia.
- **Atores:** paciente.
- **Entradas / pre-condicoes:** solicitacao realizada via perfil do paciente.
- **Fluxo esperado:** o paciente solicita alteracao, pausa ou cancelamento do plano conforme regras de negocio.
- **Saidas / pos-condicoes:** plano atualizado e confirmacao enviada ao paciente.
- **Regras relacionadas:** RNB-004, RNB-007.
- **Criterios minimos de aceite:**
  - alteracoes devem respeitar prazo minimo antes da proxima entrega
  - o sistema deve registrar a data efetiva da alteracao
  - o paciente deve receber confirmacao clara da acao executada

### 9.3 Modulo Cozinha

#### RF-010 - Painel de recebimento de pedidos

- **Descricao:** disponibilizar painel operacional em tempo real para pedidos confirmados e pagos.
- **Atores:** cozinha.
- **Entradas / pre-condicoes:** pedido confirmado e pagamento aprovado.
- **Fluxo esperado:** pedidos elegiveis aparecem no painel da cozinha com detalhes operacionais relevantes.
- **Saidas / pos-condicoes:** equipe de cozinha visualiza fila de producao atualizada.
- **Regras relacionadas:** RNB-002, RNB-004, RNB-007.
- **Criterios minimos de aceite:**
  - apenas pedidos pagos devem aparecer para producao
  - a listagem deve incluir codigo, itens e observacoes nutricionais essenciais
  - a interface deve permitir leitura rapida em contexto operacional

#### RF-011 - Gestao de producao e entrega

- **Descricao:** permitir atualizacao de status do pedido e organizacao das entregas por dias pre-definidos.
- **Atores:** cozinha.
- **Entradas / pre-condicoes:** acesso ao painel operacional e pedidos em fila.
- **Fluxo esperado:** a cozinha move o pedido pelos estados operacionais e consolida as entregas conforme a janela ativa.
- **Saidas / pos-condicoes:** status atualizado e agrupamento logico de entrega mantido.
- **Regras relacionadas:** RNB-004, RNB-007.
- **Criterios minimos de aceite:**
  - o sistema deve suportar pelo menos os estados em producao, pronto, em entrega e entregue
  - alteracoes de status devem ser auditaveis
  - a consolidacao de entrega deve respeitar regras vigentes por data ou frequencia

#### RF-017 - Previsao de demanda

- **Descricao:** apresentar consolidacao de pedidos por data de entrega para planejamento da producao.
- **Atores:** cozinha, administrador.
- **Entradas / pre-condicoes:** filtro por periodo.
- **Fluxo esperado:** o usuario consulta volume de marmitas e ingredientes previstos por janela de entrega.
- **Saidas / pos-condicoes:** relatorio consolidado de demanda por data.
- **Regras relacionadas:** RNB-004.
- **Criterios minimos de aceite:**
  - o sistema deve consolidar quantidade total de marmitas por dia
  - a saida deve apoiar previsao de ingredientes e capacidade operacional
  - filtros devem permitir recorte de periodo

### 9.4 Modulo Administrativo

#### RF-012 - Dashboard administrativo do site

- **Descricao:** oferecer painel central para gestao de usuarios, pedidos, transacoes, regras e relatorios.
- **Atores:** administrador.
- **Entradas / pre-condicoes:** autenticacao de administrador.
- **Fluxo esperado:** o administrador acessa indicadores e ferramentas de gestao global da plataforma.
- **Saidas / pos-condicoes:** dados monitorados e configuracoes administrativas disponiveis.
- **Regras relacionadas:** RNB-005, RNB-007.
- **Criterios minimos de aceite:**
  - o dashboard deve consolidar informacoes operacionais e transacionais
  - a administracao deve conseguir consultar pedidos e usuarios por filtros
  - regras gerais do sistema devem ser editaveis por usuario autorizado

#### RF-013 - Gestao de cozinhas parceiras

- **Descricao:** permitir administracao de cozinhas e parceiros operacionais.
- **Atores:** administrador.
- **Entradas / pre-condicoes:** dados das cozinhas e pedidos relacionados.
- **Fluxo esperado:** o administrador consulta desempenho, pedidos em producao e parametros operacionais das cozinhas.
- **Saidas / pos-condicoes:** configuracoes dos parceiros atualizadas.
- **Regras relacionadas:** RNB-004, RNB-007.
- **Criterios minimos de aceite:**
  - o sistema deve permitir visualizar dados cadastrais e operacionais da cozinha
  - parametros de entrega e horarios devem ser gerenciaveis
  - o desempenho operacional deve ser consultavel

#### RF-014 - Gerenciamento de comissoes

- **Descricao:** calcular e registrar a comissao progressiva do nutricionista por pedido.
- **Atores:** administrador, nutricionista.
- **Entradas / pre-condicoes:** valor base, valor final e dados do pedido.
- **Fluxo esperado:** o sistema calcula a diferenca comercial e persiste a informacao para consulta e relatorio.
- **Saidas / pos-condicoes:** comissao registrada na transacao.
- **Regras relacionadas:** RNB-003.
- **Criterios minimos de aceite:**
  - o calculo deve considerar valor base e valor final praticado
  - o valor da comissao deve permanecer rastreavel por pedido
  - relatarios devem refletir os valores registrados

#### RF-018 - Conciliacao financeira

- **Descricao:** gerar relatorios financeiros com pagamentos, comissoes e custos operacionais.
- **Atores:** administrador.
- **Entradas / pre-condicoes:** selecao de periodo.
- **Fluxo esperado:** o administrador solicita consolidacao financeira para analise e exportacao.
- **Saidas / pos-condicoes:** planilha ou relatorio exportavel com detalhamento de valores.
- **Regras relacionadas:** RNB-003, RNB-006.
- **Criterios minimos de aceite:**
  - a consulta deve consolidar pagamentos recebidos, comissoes e custos operacionais
  - o resultado deve ser exportavel
  - o recorte por periodo deve ser suportado

## 10. Regras de negocio

### RNB-001 - Operacao white label

Todos os pedidos, embalagens e experiencias voltadas ao cliente final devem priorizar a identidade visual da clinica do nutricionista, incluindo logotipo, nome e configuracoes de marca. A marca FastInBox atua como fornecedora em segundo plano.

### RNB-002 - Validacao pre-pagamento

O paciente somente pode confirmar e pagar o pedido apos revisar e validar as informacoes obrigatorias. Edicoes sao permitidas apenas antes da confirmacao final e do pagamento.

### RNB-003 - Comissao progressiva

Cada pedido possui valor base e valor final configurado, permitindo ao nutricionista ampliar sua margem. O sistema deve calcular, registrar e disponibilizar relatorios sobre a comissao de cada pedido.

### RNB-004 - Agrupamento e frequencia de entrega

Pedidos devem ser consolidados em dias ou janelas de entrega definidas pela operacao, inicialmente com possibilidade de concentracao em dias especificos e futura expansao conforme demanda.

### RNB-005 - Seguranca dos dados e autenticacao

Todo acesso e transacao deve ocorrer em ambiente seguro, com armazenamento protegido de credenciais e dados sensiveis. As informacoes devem ser protegidas por criptografia adequada e trafego sob HTTPS.

### RNB-006 - Integracao com gateway de pagamento

A plataforma deve utilizar checkout integrado, aceitando diferentes meios de pagamento sem redirecionar o usuario para dominio externo.

### RNB-007 - Acesso multi-perfil

O sistema deve garantir segregacao de acesso por perfil, liberando apenas as funcionalidades e dados autorizados para nutricionistas, pacientes, cozinhas e administradores.

## 11. Requisitos nao funcionais

### RNF-001 - Arquitetura e tecnologias

- front-end em TypeScript com React ou Next.js
- back-end em Node.js com NestJS
- banco de dados relacional, preferencialmente PostgreSQL
- codigo modular, reutilizavel, padronizado e documentado

### RNF-002 - Desempenho e escalabilidade

- a home page deve responder em ate 3 segundos em condicoes normais de operacao
- a arquitetura deve suportar crescimento de usuarios e pedidos
- o sistema deve permitir escalabilidade horizontal e vertical conforme a demanda

### RNF-003 - Seguranca

- senhas devem ser protegidas com hashing e salt
- acessos sensiveis, especialmente administrativos, devem suportar MFA
- dados sensiveis devem ser protegidos em repouso e em transito
- toda comunicacao externa deve usar HTTPS

### RNF-004 - Usabilidade e responsividade

- navegacao simples, consistente e orientada por perfil
- layout responsivo para mobile, tablet e desktop
- formularios com validacao clara, feedback imediato e prevencao de erro

### RNF-005 - Confiabilidade e disponibilidade

- a plataforma deve priorizar alta disponibilidade
- a operacao deve possuir estrategia de backup e recuperacao
- o ambiente deve suportar monitoramento e resposta rapida a falhas

### RNF-006 - Manutenibilidade e testabilidade

- base de codigo modular e de facil manutencao
- cobertura por testes unitarios, integracao e end-to-end conforme o modulo
- pipelines de CI/CD devem suportar deploys seguros

### RNF-007 - Compatibilidade e acessibilidade

- compatibilidade com navegadores modernos
- aderencia a diretrizes WCAG aplicaveis
- leitura, contraste e navegacao devem atender diferentes perfis de usuario

### RNF-008 - Monitoramento e logging

- logs de atividades e erros devem ser registrados
- eventos operacionais e tecnicos devem ser monitorados
- a rastreabilidade deve suportar auditoria e diagnostico

## 12. Matriz de perfis x capacidades

| Capacidade | Nutricionista | Paciente | Cozinha | Administrador |
| --- | --- | --- | --- | --- |
| Autenticacao | Sim | Sim ou acesso por codigo | Sim | Sim |
| Cadastrar paciente | Sim | Nao | Nao | Consulta/gestao |
| Criar pedido | Sim | Sim no autoatendimento | Nao | Consulta/gestao |
| Editar pedido antes da confirmacao | Parcial | Sim | Nao | Suporte/controlado |
| Confirmar pedido | Nao | Sim | Nao | Suporte/controlado |
| Pagar pedido | Nao | Sim | Nao | Consulta |
| Atualizar status operacional | Nao | Nao | Sim | Sim |
| Configurar identidade visual | Sim | Nao | Nao | Suporte |
| Gerir regras globais | Nao | Nao | Nao | Sim |
| Consultar relatorios financeiros | Limitado | Nao | Limitado | Sim |

## 13. Jornadas principais

### 13.1 Jornada do nutricionista

1. Autenticar na plataforma.
2. Cadastrar ou localizar paciente.
3. Montar pedido com marmitas, ingredientes, embalagem e precificacao.
4. Gerar codigo unico.
5. Compartilhar codigo com o paciente.
6. Acompanhar confirmacao, pagamento e status do pedido.

### 13.2 Jornada do paciente

1. Acessar a landing page de paciente.
2. Informar o codigo do pedido ou iniciar autoatendimento.
3. Revisar dados, ajustar quando permitido e confirmar.
4. Realizar pagamento integrado.
5. Acompanhar status de producao e entrega.

### 13.3 Jornada da cozinha

1. Acessar painel operacional.
2. Visualizar pedidos pagos.
3. Consultar detalhes nutricionais e operacionais.
4. Atualizar status de producao.
5. Consolidar pedidos por janela de entrega.
6. Finalizar entrega.

### 13.4 Jornada do administrador

1. Autenticar com privilegios administrativos.
2. Monitorar usuarios, pedidos, pagamentos e operacao.
3. Gerir cozinhas parceiras e regras do sistema.
4. Consultar relatorios financeiros e operacionais.

## 14. Inventario de telas

### 14.1 Componentes globais

| Tela / componente | Publico | Objetivo | Requisitos relacionados |
| --- | --- | --- | --- |
| NavBar | Publico geral | Navegacao principal, entradas por perfil e menu mobile | Apoio institucional |
| Footer | Publico geral | Informacoes institucionais, suporte, termos e redes | Apoio institucional |

### 14.2 Telas institucionais

| Tela | Publico | Objetivo | Requisitos relacionados |
| --- | --- | --- | --- |
| Home page | Publico geral | Apresentar proposta de valor e caminhos de entrada | Contexto institucional |
| Sobre nos | Publico geral | Comunicar historia, missao, visao e proposta de valor | Contexto institucional |
| Contato / FAQ | Publico geral | Suporte, duvidas frequentes e contato | Contexto institucional |
| Erro / 404 | Publico geral | Tratamento de rotas invalidas com redirecionamento amigavel | RNF-004 |
| Recuperacao de senha | Usuarios autenticaveis | Iniciar redefinicao segura de acesso | RF-001 |

### 14.3 Telas do nutricionista

| Tela | Objetivo | Requisitos relacionados |
| --- | --- | --- |
| Login do nutricionista | Autenticacao do perfil | RF-001 |
| Cadastro do nutricionista | Criacao de conta e dados da clinica | RF-001, RF-004 |
| Dashboard do nutricionista | Visao geral de pedidos, status e atalhos operacionais | RF-001, RF-002, RF-003, RF-004 |
| Formulario de cadastro de paciente | Criar e editar paciente | RF-002 |
| Formulario de criacao de pedido | Montar pedido e gerar codigo | RF-003 |
| Gestao de planos recorrentes | Criar e manter assinaturas | RF-015 |
| Configuracoes da clinica | Gerir logo e identidade visual | RF-004 |

### 14.4 Telas do paciente

| Tela | Objetivo | Requisitos relacionados |
| --- | --- | --- |
| Landing page de paciente | Inserir codigo do pedido | RF-005 |
| Detalhes do pedido | Revisar, editar e confirmar | RF-005, RF-006 |
| Pagamento do pedido | Concluir checkout integrado | RF-007 |
| Perfil do paciente | Consultar dados, historico e status | RF-008 |
| Autoatendimento | Montar pedido com codigo de nutricionista | RF-009 |
| Gestao de assinaturas | Alterar, pausar ou cancelar plano | RF-016 |

### 14.5 Telas da cozinha

| Tela | Objetivo | Requisitos relacionados |
| --- | --- | --- |
| Login da cozinha | Autenticacao do perfil operacional | RF-010, RNB-007 |
| Painel de pedidos | Receber pedidos pagos em tempo real | RF-010 |
| Detalhamento do pedido | Apoiar preparo, leitura de observacoes e entrega | RF-010, RF-011 |
| Planejamento de demanda | Consolidar producao por data | RF-017 |

### 14.6 Telas administrativas

| Tela | Objetivo | Requisitos relacionados |
| --- | --- | --- |
| Dashboard administrativo | Monitorar operacao e gerir configuracoes | RF-012 |
| Gestao de cozinhas e parceiros | Administrar parceiros operacionais | RF-013 |
| Gestao de comissoes | Consultar e validar calculos de margem | RF-014 |
| Conciliacao financeira | Exportar relatorios financeiros | RF-018 |

## 15. Entidades de dominio de referencia

| Entidade | Finalidade |
| --- | --- |
| Usuario | Conta de acesso do sistema, com perfil e credenciais |
| Nutricionista | Perfil profissional associado a clinica, pacientes e pedidos |
| Clinica | Identidade visual e dados comerciais usados no white label |
| Paciente | Dados cadastrais, historico e relacao com pedidos e assinaturas |
| Cozinha | Parceiro operacional responsavel por producao e entrega |
| Pedido | Registro comercial e operacional da compra |
| Item de pedido / marmita | Composicao individual do pedido |
| Ingrediente | Elemento configuravel da marmita |
| Embalagem | Tipo de embalagem selecionado no pedido |
| Pagamento | Registro transacional do checkout |
| Comissao | Valor calculado e registrado por pedido |
| Janela de entrega | Agenda de consolidacao e expedicao |
| Assinatura | Configuracao recorrente de pedidos futuros |
| Historico de status | Rastreabilidade de alteracoes operacionais |
| Log de auditoria | Registro de eventos sensiveis e acoes criticas |

## 16. Integracoes externas esperadas

| Integracao | Objetivo | Observacao |
| --- | --- | --- |
| Gateway de pagamento | Processar pagamentos integrados | Obrigatorio para RF-007 e RF-018 |
| E-mail ou canal de notificacao | Recuperacao de senha e confirmacoes | Canal exato ainda depende de definicao |
| Hospedagem front-end | Publicacao da aplicacao web | Vercel prevista |
| Hospedagem back-end | Publicacao da API e servicos | Railway ou Heroku previstos |

## 17. Requisitos de seguranca, auditoria e compliance

- autenticar e autorizar usuarios com segregacao por perfil
- proteger senhas com algoritmo seguro e parametrizacao atualizavel
- proteger dados sensiveis em repouso e em transito
- registrar eventos sensiveis como login, redefinicao de senha, pagamento e mudanca de status
- limitar exposicao de dados pessoais ao minimo necessario por perfil
- suportar trilha de auditoria para operacoes administrativas e financeiras

## 18. Criticidade e sugestao de faseamento

### 18.1 Escopo essencial de MVP

- RF-001 a RF-008
- RF-010 a RF-014
- RNB-001 a RNB-007
- RNF-001 a RNF-008

### 18.2 Escopo evolutivo recomendado

- RF-009 autoatendimento completo
- RF-015 e RF-016 assinaturas
- RF-017 previsao de demanda avancada
- RF-018 conciliacao financeira expandida

## 19. Riscos e pontos de atencao

- definicao tardia do gateway pode impactar checkout, conciliacao e experiencia do paciente
- regras insuficientemente detalhadas de entrega podem gerar inconsistencias na consolidacao da cozinha
- ausencia de definicao formal de notificacoes pode afetar recuperacao de senha e comunicacao transacional
- personalizacao white label exige governanca para evitar conflito entre marca da clinica e marca da plataforma
- modulos financeiros e de assinatura exigem validacao adicional de regras antes da implementacao final

## 20. Pendencias para validacao executiva e tecnica

- definir responsaveis oficiais por produto, design, front-end e back-end
- definir gateway de pagamento e meios aceitos
- definir canais oficiais de notificacao transacional
- definir regras completas de SLA operacional e disponibilidade
- definir regras exatas de antecedencia para alteracao de assinaturas
- definir parametros de entrega por regiao, cozinha e janela
- definir estrategia de impressao ou aplicacao da identidade visual nas embalagens

## 21. Criterio de encerramento desta fase documental

Esta ERS deve ser considerada validada quando:

1. produto confirmar escopo, prioridades e pendencias
2. design validar o inventario de telas e jornadas
3. engenharia validar viabilidade tecnica e dependencias externas
4. operacoes validar regras de producao, entrega e conciliacao

