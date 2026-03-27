# FastInBox - MVP Canvas

**Framework de referencia:** MVP Canvas de Paulo Caroli  
**Produto:** FastInBox  
**Versao:** 1.0  
**Data:** 2026-03-27  
**Status:** Draft para validacao executiva e tecnica  
**Classificacao:** Confidencial

## 1. Proposta do MVP

Validar um fluxo white label ponta a ponta em que o nutricionista monta um pedido personalizado de marmitas, o paciente revisa e paga dentro da plataforma, e a cozinha recebe apenas pedidos pagos para producao e entrega.

Em termos praticos, este MVP deve comprovar que:

- nutricionistas aceitam usar a plataforma para cadastrar pacientes e gerar pedidos personalizados
- pacientes conseguem concluir a revisao e o pagamento com clareza e confianca
- a operacao consegue rastrear o pedido da criacao ate a entrega sem controle manual paralelo
- o modelo white label aumenta a percepcao de continuidade entre clinica e experiencia do paciente

## 2. Personas Segmentadas

### Persona primaria

**Nutricionista parceiro / clinica parceira**

- quer vender marmitas personalizadas com sua propria marca
- precisa reduzir operacao manual em WhatsApp, planilhas e retrabalho
- precisa acompanhar status do pedido sem depender de comunicacao informal

### Persona secundaria

**Paciente da clinica**

- quer revisar o pedido com seguranca e entender exatamente o que esta comprando
- espera uma experiencia simples, confiavel e coerente com a identidade da clinica
- precisa pagar sem friccao e acompanhar a evolucao do pedido

### Persona operacional

**Cozinha parceira**

- precisa receber apenas pedidos validos e pagos
- precisa consultar rapidamente itens, observacoes e status
- precisa atualizar producao e entrega de forma rastreavel

### Persona de governanca

**Administrador FastInBox**

- precisa monitorar operacao, pedidos, usuarios e regras globais
- precisa visibilidade minima sobre comissoes, pagamentos e parceiros

## 3. Jornadas

### Jornada 1: nutricionista cria pedido

1. Nutricionista autentica na plataforma.
2. Cadastra ou seleciona um paciente.
3. Monta um pedido com uma ou mais marmitas, embalagem e precificacao.
4. Gera um codigo unico de acesso ao pedido.
5. Compartilha o codigo com o paciente.

### Jornada 2: paciente revisa e paga

1. Paciente acessa a landing page de pedido.
2. Informa o codigo unico recebido.
3. Revisa dados do pedido e faz ajustes permitidos antes da confirmacao.
4. Confirma as informacoes.
5. Realiza o pagamento no checkout integrado.
6. Consulta o status do pedido.

### Jornada 3: cozinha executa operacao

1. Cozinha acessa o painel operacional.
2. Visualiza apenas pedidos pagos.
3. Consulta detalhes do pedido.
4. Atualiza os status operacionais.
5. Consolida a entrega conforme a janela definida.

## 4. Funcionalidades do MVP

### Bloco produto

- autenticacao por perfil
- recuperacao segura de senha
- rotas protegidas e segregacao de acesso
- cadastro e edicao de pacientes pelo nutricionista
- criacao de pedido com multiplas marmitas
- calculo de valor base, valor final e comissao
- geracao e validacao de codigo unico do pedido
- configuracao basica de identidade visual da clinica
- landing do paciente com acesso por codigo
- revisao, edicao controlada e confirmacao do pedido
- checkout integrado sem redirecionamento externo
- historico e status resumido do pedido para o paciente
- painel operacional da cozinha
- atualizacao auditavel de status operacionais
- dashboard administrativo basico

### Bloco de suporte tecnico

- arquitetura base front-end e back-end
- banco relacional com migracoes iniciais
- logs e auditoria de eventos sensiveis
- pipeline CI/CD inicial
- provisionamento de banco e storage
- estrategia minima de testes e quality gates

## 5. Resultado Esperado

O MVP sera considerado validado se demonstrar, em ambiente real controlado ou piloto:

- capacidade de gerar pedidos white label sem dependencia de controle manual externo
- conclusao do fluxo paciente -> confirmacao -> pagamento com taxa de sucesso aceitavel
- liberacao automatica apenas de pedidos pagos para a cozinha
- visibilidade operacional minima para nutricionista, cozinha e administracao
- reducao perceptivel de friccao operacional frente ao processo manual atual

## 6. Metricas para Validar as Hipoteses de Negocio

### Hipotese 1

Nutricionistas aceitarao usar a plataforma para substituir parte relevante da operacao manual de pedidos.

**Metricas**

- quantidade de nutricionistas ativos no piloto
- quantidade de pacientes cadastrados por nutricionista
- quantidade de pedidos criados por nutricionista
- tempo medio para montar e gerar um pedido

### Hipotese 2

Pacientes conseguem revisar e pagar o pedido sem alto indice de abandono.

**Metricas**

- taxa de acesso ao pedido por codigo
- taxa de confirmacao apos acesso
- taxa de conversao de pagamento
- taxa de abandono entre revisao e checkout
- tempo medio entre acesso e pagamento

### Hipotese 3

O fluxo operacional da cozinha fica mais confiavel quando recebe apenas pedidos pagos e estruturados.

**Metricas**

- quantidade de pedidos pagos recebidos pela cozinha
- tempo medio entre pagamento aprovado e disponibilidade operacional
- percentual de pedidos com status atualizado corretamente
- quantidade de inconsistencias operacionais reportadas

### Hipotese 4

O white label aumenta a confianca do paciente e a aderencia ao fluxo.

**Metricas**

- taxa de conclusao em pedidos com identidade visual aplicada
- feedback qualitativo de pacientes e nutricionistas
- volume de suporte ou duvida relacionado a confianca no processo

## 7. Custo e Cronograma

### Escopo recomendado desta versao

Este MVP deve focar somente no fluxo essencial:

- nutricionista cadastra paciente e cria pedido
- paciente acessa por codigo, revisa, confirma e paga
- cozinha recebe pedidos pagos e atualiza status
- administrador consulta operacao basica

### Itens fora do MVP imediato

- autoatendimento completo do paciente
- assinaturas recorrentes
- previsao de demanda avancada
- conciliacao financeira expandida
- integracoes fiscais e ERP
- aplicativo mobile nativo

### Proposta de faseamento

**Fase 1 - Fundacao**

- arquitetura base
- autenticacao
- infraestrutura inicial
- design system
- definicoes de produto e regras de acesso

**Fase 2 - Nucleo comercial**

- pacientes
- pedidos
- comissao
- branding white label

**Fase 3 - Conversao e operacao**

- acesso por codigo
- revisao e confirmacao
- pagamento
- painel da cozinha

**Fase 4 - Governanca minima**

- dashboard administrativo
- relatorios basicos
- auditoria
- hardening e preparacao de go-live

### Estimativa executiva

Considerando o time atual:

- **Thiago:** produto tecnico, front-end, back-end e QA de apoio
- **Joao Vitor:** DevOps e infraestrutura
- **Gabriel:** design e definicao visual

O recorte de MVP e viavel em **1 ciclo de estruturacao + 1 ciclo de nucleo funcional + 1 ciclo de pagamento/operacao + 1 ciclo de estabilizacao**, desde que o gateway de pagamento e as regras logisticas sejam definidos sem atraso.

## Hipotese central resumida

Se entregarmos um fluxo white label simples, seguro e rastreavel para pedido personalizado de marmitas, entao nutricionistas conseguirao vender com menos operacao manual, pacientes conseguirao concluir o pedido com mais confianca, e a cozinha operara com menos ruído e mais previsibilidade.

## Recomendacao executiva

Nao ampliar o escopo antes de validar:

- adesao do nutricionista ao fluxo de criacao do pedido
- conversao do paciente entre revisao e pagamento
- consistencia operacional da cozinha com status e entrega

O sucesso deste MVP depende mais da clareza do fluxo e da disciplina de validacao do que da quantidade de funcionalidades.
