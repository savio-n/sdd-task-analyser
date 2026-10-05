# SDD Specification — Task Analyser

## 1. Visão geral e contrato de negócio

### 1.1 Identificação

**Projeto:** Task Analyser – Módulo de Métricas e Produtividade
**Autor:** SÁVIO ARBUÊS ABRAHÃO NERY
**Curso:** Ciência de Dados e Machine Learning
**Versão:** 1.0
**Data:** 27/08/2026

### 1.2 Propósito

O **Task Analyser** é um módulo de análise de tarefas e produtividade desenvolvido para transformar dados de execução de tarefas em métricas objetivas que auxiliem na avaliação de desempenho, pontualidade e utilização de recursos.

O módulo recebe um conjunto de tarefas e produz indicadores quantitativos que permitem identificar:

* padrões de produtividade;
* atrasos;
* distribuição das tarefas por prioridade;
* utilização de recursos computacionais.

O desenvolvimento segue o paradigma de **Spec-Driven Development (SDD)**. Esta especificação representa o contrato técnico e funcional que orienta a implementação.

### Escopo funcional

O módulo deverá contemplar:

* cálculo do tempo médio de conclusão das tarefas;
* cálculo da taxa de atraso;
* geração de indicadores agrupados por prioridade;
* cálculo de métricas relacionadas ao uso de recursos computacionais;
* geração de alertas quando determinados limites de utilização de recursos forem atingidos;
* validação dos dados de entrada;
* tratamento controlado de situações de erro;
* produção de resultados estruturados para consumo pelos demais componentes do sistema.

O módulo **não deverá persistir dados** em arquivos ou bancos de dados nesta fase. Os dados deverão ser processados exclusivamente em memória.

---

## 2. Contrato executável de interface

A implementação, inclusive código produzido por ferramentas de Inteligência Artificial, deverá respeitar as entradas, saídas, tipos de dados e regras estabelecidas nesta especificação.

### 2.1 Estrutura das entradas

Cada tarefa deverá possuir os seguintes campos:

| Campo               | Tipo            | Obrigatório | Descrição                                          | Restrições                                          |
| ------------------- | --------------- | ----------- | -------------------------------------------------- | --------------------------------------------------- |
| `id`                | `str` ou `int`  | Sim         | Identificador da tarefa                            | Deve ser único e não nulo                           |
| `title`             | `str`           | Sim         | Título da tarefa                                   | Não pode ser vazio                                  |
| `priority`          | `str`           | Sim         | Prioridade                                         | `alta`, `media` ou `baixa`                          |
| `created_at`        | `str`           | Sim         | Data/hora de criação                               | Deve representar uma data válida                    |
| `due_date`          | `str`           | Sim         | Prazo da tarefa                                    | Deve ser válida e igual ou posterior a `created_at` |
| `completed_at`      | `str` ou `None` | Condicional | Data/hora de conclusão                             | Obrigatório quando a tarefa estiver concluída       |
| `status`            | `str`           | Sim         | Estado da tarefa                                   | `pendente`, `em_andamento` ou `concluida`           |
| `cpu_usage_percent` | `float`         | Não         | Utilização de CPU associada à tarefa/processamento | Deve estar entre 0 e 100                            |

### 2.2 Formato das datas

As datas deverão utilizar formato compatível com **ISO 8601**, preferencialmente:

```text
YYYY-MM-DDTHH:MM:SS
```

Informações de fuso horário poderão ser incluídas conforme o padrão ISO 8601.

---

## 3. Estrutura das saídas

A função principal deverá retornar um objeto estruturado contendo as métricas calculadas:

```python
{
    "tempo_medio_conclusao_horas": float | None,
    "taxa_atraso_percentual": float,
    "total_tarefas_analisadas": int,
    "total_tarefas_concluidas": int,
    "total_tarefas_atrasadas": int,
    "indicadores_por_prioridade": {
        "alta": {
            "quantidade": int,
            "tempo_medio_conclusao_horas": float | None,
            "taxa_atraso_percentual": float
        },
        "media": {
            "quantidade": int,
            "tempo_medio_conclusao_horas": float | None,
            "taxa_atraso_percentual": float
        },
        "baixa": {
            "quantidade": int,
            "tempo_medio_conclusao_horas": float | None,
            "taxa_atraso_percentual": float
        }
    },
    "recursos": {
        "cpu_media_percentual": float,
        "alerta_cpu": bool
    }
}
```

Os nomes dos campos acima constituem parte do contrato e não deverão ser alterados sem autorização.

---

## 4. Regras de cálculo

### 4.1 Tempo médio de conclusão

Para cada tarefa concluída:

```text
tempo de conclusão = completed_at - created_at
```

O resultado deverá ser convertido para horas.

O tempo médio será calculado somente considerando tarefas concluídas.

Caso não exista nenhuma tarefa concluída, `tempo_medio_conclusao_horas` deverá assumir o valor `None`, evitando divisão por zero.

### 4.2 Taxa de atraso

Uma tarefa concluída será considerada atrasada quando:

```text
completed_at > due_date
```

A taxa de atraso geral será:

```text
(quantidade de tarefas atrasadas / quantidade de tarefas concluídas) × 100
```

Caso não existam tarefas concluídas, a taxa de atraso deverá ser `0.0`.

### 4.3 Indicadores por prioridade

As métricas deverão ser agrupadas pelas prioridades:

* `alta`;
* `media`;
* `baixa`.

Para cada prioridade deverão ser informados:

* quantidade de tarefas;
* tempo médio de conclusão das tarefas concluídas daquela prioridade;
* taxa de atraso das tarefas daquela prioridade.

Caso uma determinada prioridade não possua tarefas concluídas:

* `tempo_medio_conclusao_horas` deverá ser `None`;
* `taxa_atraso_percentual` deverá ser `0.0`.

### 4.4 Métrica de utilização de CPU

O sistema deverá calcular a média dos valores de `cpu_usage_percent` informados nas tarefas.

O percentual deverá permanecer no intervalo de **0 a 100**.

O limite padrão para geração de alerta será de **80%**.

Quando a média de utilização de CPU atingir ou ultrapassar 80%:

```text
alerta_cpu = True
```

Caso contrário:

```text
alerta_cpu = False
```

### 4.5 Arredondamento

Os valores percentuais e médias numéricas deverão ser arredondados para **duas casas decimais**, quando aplicável.

---

## 5. Validação e tratamento de erros

Os dados de entrada deverão ser validados antes dos cálculos.

As seguintes situações deverão gerar erros controlados:

* lista de tarefas vazia;
* campo obrigatório ausente;
* identificador nulo ou inválido;
* título vazio;
* prioridade diferente de `alta`, `media` ou `baixa`;
* status diferente de `pendente`, `em_andamento` ou `concluida`;
* data em formato inválido;
* `created_at` posterior a `due_date`;
* tarefa concluída sem `completed_at`;
* `completed_at` anterior a `created_at`;
* `cpu_usage_percent` menor que 0 ou maior que 100.

Para dados inválidos deverá ser utilizada uma exceção específica, preferencialmente `ValueError`, acompanhada de mensagem clara.

O sistema não deverá utilizar exceções genéricas como mecanismo principal de controle de fluxo.

---

## 6. Função pública principal

A implementação deverá disponibilizar:

```python
def analyze_tasks(tasks: list[dict]) -> dict:
    """Analisa um conjunto de tarefas e calcula métricas de produtividade."""
```

A função deverá:

* receber uma lista de dicionários;
* validar os dados;
* calcular as métricas;
* retornar o dicionário definido neste contrato.

A assinatura, o nome da função e seus parâmetros não deverão ser modificados sem autorização.

---

# 7. Cenários de aceite

## 7.1 Cenário 1 — Análise realizada com sucesso

**Dado** um conjunto de cinco tarefas válidas contendo:

* três tarefas concluídas dentro do prazo;
* uma tarefa concluída após o prazo;
* uma tarefa pendente dentro do prazo;
* tarefas distribuídas entre as prioridades alta, média e baixa;
* valores válidos de utilização de CPU.

**Quando** `analyze_tasks` for executada.

**Então** o sistema deverá:

* retornar as métricas sem lançar exceção;
* calcular corretamente o tempo médio das tarefas concluídas;
* identificar corretamente a quantidade de tarefas atrasadas;
* calcular a taxa de atraso;
* gerar os indicadores por prioridade;
* calcular a média de utilização de CPU;
* indicar corretamente se o limite de CPU foi atingido.

## 7.2 Cenário 2 — Dados inválidos

**Dado** um conjunto contendo uma tarefa cuja data de conclusão seja anterior à data de criação.

**Quando** `analyze_tasks` for executada.

**Então** o sistema deverá:

* rejeitar a entrada;
* lançar `ValueError`;
* apresentar mensagem clara indicando que os dados de data são inválidos;
* não produzir métricas incorretas.

## 7.3 Cenário 3 — Lista vazia

**Dado** que nenhuma tarefa foi fornecida.

**Quando** `analyze_tasks` for executada.

**Então** o sistema deverá:

* rejeitar a entrada;
* lançar `ValueError`;
* informar claramente que nenhuma tarefa foi fornecida.

## 7.4 Cenário 4 — Prioridade inválida

**Dado** uma tarefa contendo:

```python
priority = "urgente"
```

**Quando** `analyze_tasks` for executada.

**Então** o sistema deverá:

* rejeitar a tarefa;
* lançar `ValueError`;
* informar que a prioridade não é válida;
* não incluir a tarefa nos cálculos.

## 7.5 Cenário 5 — Alerta de utilização de CPU

**Dado** um conjunto de tarefas válidas cuja utilização média de CPU seja igual ou superior a 80%.

**Quando** o analisador calcular as métricas.

**Então** o sistema deverá:

* calcular corretamente a média;
* definir `alerta_cpu` como `True`;
* disponibilizar essa informação no resultado.

---

# 8. Test Harness

Na Fase 2, os cenários de aceite serão transformados em testes automatizados utilizando **Python e pytest**.

O Test Harness deverá:

1. criar dados de teste representativos;
2. testar as métricas;
3. utilizar `pytest.raises` para validar exceções;
4. validar os valores retornados;
5. validar prioridades e atrasos;
6. validar métricas de CPU e alertas;
7. testar caminhos de sucesso;
8. testar casos de erro;
9. testar casos de borda.

O fluxo de validação será:

```text
Especificação SDD
        ↓
Cenários de aceite
        ↓
Testes pytest
        ↓
Código gerado pela IA
        ↓
Execução do Test Harness
        ↓
Homologação humana
        ↓
Commit
```

Os testes não deverão ser modificados simplesmente para fazer uma implementação incorreta ser aprovada.

---

# 9. Governança para agentes de IA

## 9.1 Padrões obrigatórios

O projeto deverá utilizar:

* Python 3.12 ou superior;
* Type Hints em todas as funções e métodos;
* Clean Code;
* SRP (Single Responsibility Principle);
* PEP 8;
* Google Style Docstrings;
* funções pequenas e coesas;
* nomes descritivos;
* tratamento específico de exceções;
* `logging` para registros relevantes.

## 9.2 Regras para IA

Os agentes de IA deverão:

1. utilizar esta especificação como fonte principal de requisitos;
2. respeitar o contrato de entrada e saída;
3. implementar somente comportamentos definidos;
4. preservar assinaturas públicas;
5. manter compatibilidade com Python 3.12+;
6. sinalizar ambiguidades antes de assumir comportamentos;
7. criar testes correspondentes às funcionalidades.

## 9.3 Restrições

Os agentes de IA não poderão:

* alterar arbitrariamente os requisitos;
* alterar nomes ou parâmetros de funções públicas sem autorização;
* modificar cenários de aceite para fazer testes passarem artificialmente;
* persistir dados em arquivos ou bancos;
* utilizar bibliotecas externas não autorizadas;
* assumir comportamentos não definidos;
* ignorar erros de validação;
* utilizar `except Exception: pass`;
* inserir credenciais, senhas ou tokens;
* criar funcionalidades não solicitadas.

---

# 10. Rastreabilidade

Toda implementação deverá ser rastreável aos requisitos desta especificação.

Quando houver alteração no código, deverá ser possível identificar:

* qual requisito motivou a alteração;
* quais testes validam o comportamento;
* qual regra de negócio está sendo atendida.

Informações externas ou suposições não deverão ser tratadas como requisitos do sistema.

---

# 11. Homologação humana

A utilização de Inteligência Artificial não elimina a necessidade de revisão humana.

Antes da aprovação, deverá ser verificado:

### Validação funcional

* tempo médio;
* taxa de atraso;
* indicadores por prioridade;
* CPU;
* alertas;
* validações;
* exceções.

### Conformidade

* entradas;
* saídas;
* regras de negócio;
* assinaturas públicas;
* ausência de comportamentos não especificados.

### Qualidade

* legibilidade;
* organização;
* nomes;
* SRP;
* PEP 8;
* Type Hints;
* Google Style Docstrings;
* tratamento de exceções;
* logs;
* ausência de código desnecessário.

### Casos de borda

* uma única tarefa;
* todas as tarefas concluídas;
* nenhuma tarefa concluída;
* diferentes prioridades;
* tarefa exatamente no prazo;
* tarefa atrasada;
* CPU exatamente no limite;
* CPU acima do limite;
* entradas inválidas.

A decisão final sobre a aceitação do código será sempre humana.

---

# 12. Observação sobre a implementação da Fase 2

A especificação original da Fase 1 utiliza `ValueError` para erros de validação.

Caso a implementação da Fase 2 utilize uma exceção específica denominada `TaskValidationError`, ela deverá manter compatibilidade semântica com o contrato de validação definido nesta especificação.

A implementação também deverá respeitar os requisitos específicos da atividade da Fase 2 quanto à estrutura do repositório e ao Test Harness.

---

# 13. Considerações finais

Esta especificação estabelece o contrato técnico e funcional inicial do módulo **Task Analyser**.

A Fase 1 concentra-se no planejamento, especificação e governança. A implementação será realizada nas fases posteriores.

O objetivo da abordagem SDD é garantir que o desenvolvimento seja orientado por requisitos claros e verificáveis, permitindo o uso controlado de ferramentas de Inteligência Artificial.

Os cenários de aceite e o Test Harness servirão como mecanismos de validação do código produzido, enquanto a homologação humana permanecerá obrigatória para garantir a responsabilidade técnica sobre o resultado final.
