# IndicadorMP — Especificação do Painel de Métricas (página Início)

## 1. Enquadramento

O IndicadorMP não é produto comercial: não há receita, aquisição ou churn. A adaptação do framework mantém a lógica (uma métrica-farol, poucos indicadores de entrada que a movem, guardrails de saúde) e troca o objeto: em vez de valor entregue ao cliente, **direito restabelecido no território**.

Critérios aplicados a cada métrica (Yoskovitz): compreensível, comparativa, expressa em razão ou taxa, e capaz de mudar comportamento.

## 2. North Star Metric

**Taxa de resolutividade entre ciclos** = não conformidades sanadas ÷ (sanadas + persistentes), apuradas nas unidades com dois ciclos.

- Valor atual: **22,9%** (156 sanadas de 682 comparáveis, em 92 unidades).
- Por que é a métrica-farol: traduz a Recomendação CNMP-CN nº 02/2018 — resolutividade medida pela melhoria efetiva do indicador, não pelo número de expedientes.
- É comparativa (exige dois ciclos), é razão, e muda comportamento: se sobe, a atuação funcionou; se cai, a estratégia precisa mudar.
- Meta sugerida para o próximo ciclo: **35%**, com eliminação integral das persistentes de severidade alta.

## 3. Input Metrics — as alavancas

| Métrica | Definição | Fonte | Visualização | Meta | Alerta |
|---|---|---|---|---|---|
| Persistentes de severidade alta | Nº de NC alta presentes nos dois ciclos | REL_DATA × ciclo anterior | Número + barra | 0 | > 100 |
| Não conformidades novas | NC presentes só no ciclo atual | idem | Número + variação | ≤ sanadas | novas > sanadas |
| Cobertura de inspeção | Unidades inspecionadas ÷ unidades conhecidas | REL_DATA | Razão | 100% | < 90% |
| Densidade de achados | NC ÷ unidade inspecionada | REL_DATA | Número | queda contínua | alta > 8,0 |

Valores atuais: 132 persistentes altas · 171 novas contra 156 sanadas · 92 de 97 unidades com histórico · 7,5 NC por unidade.

## 4. Health Metrics — guardrails

| Métrica | Valor atual | Alerta |
|---|---|---|
| Eixos sem inspeção no ciclo | ILPI (pendente) | qualquer eixo obrigatório sem inspeção |
| Unidades sem ciclo anterior | 5 (4 Conselhos Tutelares + 1 Família Acolhedora) | > 10% da base |
| Bases externas desatualizadas | Censo SUAS 2024, PNTP 2025 | coleta vencida no calendário |
| Severidade alta pendente | 202 | crescimento entre ciclos |

## 5. Métricas de contexto (substituem as "business metrics")

Cobertura territorial (16 municípios, 12 comarcas), rede documental apurada (74 serviços do SUAS com 365 apontamentos) e transparência municipal (PNTP). Não medem desempenho do painel; dimensionam a demanda.

## 6. Layout da página Início

```
┌───────────────────────────────────────────────────────────┐
│ IndicadorMP · Inspeção que vira dado. Dado que vira ação.  │
├───────────────────────────────────────────────────────────┤
│ FAROL  Taxa de resolutividade  22,9%   ▲ meta 35%          │
│        156 sanadas · 526 persistentes · 92 unidades        │
├──────────────┬──────────────┬──────────────┬──────────────┤
│ Persistentes │ Novas        │ Cobertura    │ Densidade    │
│ alta 132     │ 171          │ 92/97        │ 7,5 NC/unid. │
├──────────────┴──────────────┴──────────────┴──────────────┤
│ SAÚDE  eixos sem inspeção · sem histórico · alta pendente  │
├───────────────────────────────────────────────────────────┤
│ O que inspecionamos │ O que contextualiza │ O que entregamos│
├───────────────────────────────────────────────────────────┤
│ 01 Inspecionar › 02 Medir › 03 Priorizar › 04 Atuar › 05 …│
└───────────────────────────────────────────────────────────┘
```

## 7. Cadência de revisão

- **Mensal** — saúde: coletas vencidas no calendário, eixos sem inspeção.
- **Semestral** — input metrics, ao fim de cada ciclo de inspeção.
- **Anual** — North Star e recalibração de metas, com o ciclo completo fechado.

## 8. Alertas

| Gatilho | Destinatário | Prazo |
|---|---|---|
| Novas > sanadas no ciclo | Corregedoria-Geral | reunião do ciclo seguinte |
| Persistente de severidade alta em 2 ciclos | Órgão de execução + CAO | 30 dias |
| Eixo obrigatório sem inspeção | Corregedoria-Geral | programação imediata |
| Coleta de base vencida | Equipe do painel | 15 dias |

## 9. Métricas descartadas por serem vaidosas

Número absoluto de apontamentos (cresce com a cobertura, não com o problema), total de unidades inspecionadas (esforço, não resultado) e o antigo score de penalidade (número sem denominador, já retirado do painel).
