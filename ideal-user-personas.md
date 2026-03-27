# FastInBox - Personas de Referencia em IHC

## Objetivo

Este documento define 4 personas de referencia do FastInBox sob a perspectiva de Interacao Humano-Computador (IHC). O objetivo e orientar decisoes de UX, UI, arquitetura da informacao, fluxo operacional e priorizacao de funcionalidades com foco em contexto de uso, comportamento, limitacoes e necessidades reais de cada perfil.

## Premissas de IHC

- cada persona representa um padrao de comportamento relevante para o MVP
- o sistema deve minimizar carga cognitiva, risco de erro e dependencia de suporte
- a experiencia deve privilegiar clareza, previsibilidade, feedback e controle
- a interface precisa respeitar o contexto operacional de cada perfil

## 1. Persona - Nutricionista Parceira

**Nome:** Dra. Mariana Alves  
**Idade:** 34 anos  
**Perfil:** nutricionista clinica, atendimento particular, orientada a relacionamento e resultado  
**Familiaridade digital:** media a alta  
**Dispositivo principal:** notebook no consultorio, celular para acompanhamentos rapidos

**Contexto de uso**

Utiliza a plataforma entre consultas e em janelas curtas de tempo. Alterna entre atendimento clinico, agenda, WhatsApp e tarefas administrativas.

**Objetivos**

- cadastrar pacientes rapidamente
- montar pedidos personalizados sem retrabalho
- preservar a identidade da propria clinica
- acompanhar confirmacao e pagamento com clareza

**Dores**

- excesso de etapas para tarefas simples
- risco de errar dados de paciente ou pedido
- dificuldade para enxergar status do pedido
- processos manuais dispersos em varias ferramentas

**Necessidades de IHC**

- fluxo curto e altamente guiado
- formularios com validacao clara e prevencao de erro
- feedback imediato apos salvar, gerar codigo ou compartilhar pedido
- hierarquia visual forte para status e proximas acoes

**Criterios de sucesso**

- concluir um pedido com seguranca em poucos minutos
- saber exatamente o que esta pendente sem precisar investigar

## 2. Persona - Paciente Final

**Nome:** Camila Rocha  
**Idade:** 29 anos  
**Perfil:** profissional com rotina intensa, busca conveniencia e confianca  
**Familiaridade digital:** media  
**Dispositivo principal:** celular

**Contexto de uso**

Interage com a plataforma em momentos curtos, geralmente por link recebido. Costuma estar em deslocamento, no trabalho ou em casa, com baixa tolerancia a fluxos confusos.

**Objetivos**

- entender o pedido com clareza
- revisar ingredientes, observacoes e valor final
- confirmar e pagar sem inseguranca
- acompanhar o status da entrega

**Dores**

- medo de confirmar um pedido com informacao errada
- desconfianca em fluxos de pagamento pouco claros
- dificuldade de leitura em telas poluidas
- frustracao com termos tecnicos ou excesso de informacao

**Necessidades de IHC**

- linguagem simples e objetiva
- alta legibilidade e contraste
- passos visiveis e previsiveis
- confirmacoes claras antes de acoes irreversiveis

**Criterios de sucesso**

- revisar tudo sem precisar pedir ajuda
- pagar com confianca e entender o que acontece depois

## 3. Persona - Operadora de Cozinha

**Nome:** Juliana Santos  
**Idade:** 38 anos  
**Perfil:** lider operacional, focada em velocidade, padronizacao e controle  
**Familiaridade digital:** media  
**Dispositivo principal:** desktop ou tablet no ambiente operacional

**Contexto de uso**

Opera sob pressao, com alto volume e necessidade de consulta rapida. O ambiente e dinamico, com interrupcoes frequentes e baixa tolerancia a interfaces lentas ou ambiguidade.

**Objetivos**

- visualizar pedidos pagos sem atraso
- entender rapidamente composicao e observacoes
- atualizar status com poucos cliques
- reduzir erro na producao e expedicao

**Dores**

- interfaces com informacao demais e pouca prioridade visual
- risco de perder detalhes nutricionais importantes
- dificuldade para distinguir pedidos por urgencia ou etapa

**Necessidades de IHC**

- leitura escaneavel
- status muito evidentes
- detalhamento objetivo e sem ruido
- acoes operacionais simples, consistentes e robustas

**Criterios de sucesso**

- localizar o pedido certo rapidamente
- executar e atualizar a operacao sem ambiguidade

## 4. Persona - Gestora Administrativa

**Nome:** Fernanda Lima  
**Idade:** 41 anos  
**Perfil:** gestora de operacao, orientada a indicadores, governanca e previsibilidade  
**Familiaridade digital:** alta  
**Dispositivo principal:** notebook

**Contexto de uso**

Usa a plataforma para monitorar saude da operacao, acompanhar excecoes e ajustar regras. Costuma trabalhar com varias fontes de informacao ao mesmo tempo e precisa de consolidacao confiavel.

**Objetivos**

- acompanhar pedidos, pagamentos e producao
- identificar gargalos rapidamente
- ajustar regras operacionais com seguranca
- obter visao consolidada para tomada de decisao

**Dores**

- falta de visao centralizada
- dificuldade em encontrar anomalias sem filtrar manualmente
- baixa rastreabilidade de mudancas e estados

**Necessidades de IHC**

- dashboards enxutos e orientados a decisao
- filtros praticos e consistentes
- rastreabilidade de status e regras
- informacao consolidada sem excesso de detalhe irrelevante

**Criterios de sucesso**

- responder rapidamente o que esta atrasado, parado ou fora do fluxo esperado
- tomar decisoes com base em dados claros e confiaveis

## Diretrizes de uso em UX

Ao desenhar fluxos, escrever microcopy ou priorizar backlog, considerar estas perguntas:

1. a tarefa principal da persona esta clara na tela?
2. o sistema reduz chance de erro humano?
3. o feedback da acao e imediato e compreensivel?
4. a interface respeita o contexto de uso e o dispositivo principal?

## Ordem de priorizacao para o MVP

1. Nutricionista Parceira
2. Paciente Final
3. Operadora de Cozinha
4. Gestora Administrativa
