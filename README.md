# SDD Task Analyser

Projeto desenvolvido para o Bootcamp III – Ciência de Dados e Machine Learning, seguindo a abordagem de Spec-Driven Development (SDD).

## Projeto

O **Task Analyser** é um módulo destinado à análise de tarefas e geração de métricas de produtividade, incluindo:

* tempo médio de conclusão;
* taxa de atraso;
* quantidade de tarefas analisadas;
* quantidade de tarefas concluídas;
* quantidade de tarefas atrasadas;
* indicadores por prioridade;
* utilização média de CPU;
* alertas relacionados ao uso de CPU.

A implementação é orientada pela especificação definida na **Fase 1** do projeto.

## Objetivo da Fase 2

Esta etapa tem como objetivo implementar a solução utilizando assistência de Inteligência Artificial, criar um **Test Harness com pytest** e aplicar boas práticas de versionamento com **Git e GitHub**.

### Estrutura do projeto

```text
sdd-task-analyser/
├── README.md
├── CONTEXT_RULES.md
├── .gitignore
├── requirements.txt
├── specs/
│   └── task_analyzer_spec.md
├── tests/
│   └── test_harness.py
└── src/
    └── task_analyzer.py
```

## Tecnologias

* Python 3.12+
* pytest
* Git
* GitHub
* Assistentes de Inteligência Artificial

## Metodologia

O desenvolvimento segue os princípios de **Spec-Driven Development**, utilizando a especificação como contrato técnico e funcional para orientar:

1. implementação;
2. validação;
3. testes automatizados;
4. revisão humana;
5. versionamento da solução.

## Validação

A solução será validada por meio de um **Test Harness desenvolvido com pytest**, contemplando os cenários de aceitação definidos na especificação do projeto.

## Autor

**Sávio Arbuês Abrahão Nery**

Ciência de Dados e Machine Learning
