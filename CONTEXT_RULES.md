# CONTEXT RULES — Task Analyser

## 1. Objetivo

Estas regras definem as restrições e orientações que devem ser seguidas por qualquer assistente de Inteligência Artificial utilizado no desenvolvimento do projeto **Task Analyser**.

A especificação funcional e técnica do projeto é a fonte de verdade para a implementação.

---

## 2. Fonte de verdade

A implementação deve seguir prioritariamente:

1. `specs/task_analyzer_spec.md`
2. Os cenários de aceitação definidos na Fase 1
3. Estas regras de contexto
4. Requisitos explícitos da atividade do Bootcamp III

A IA não deve inventar requisitos ou comportamentos que não estejam definidos nesses documentos.

---

## 3. Regras de implementação

A IA deve:

* preservar o contrato funcional definido pela especificação;
* preservar os nomes dos campos de entrada e saída;
* preservar a assinatura pública da função `analyze_tasks`;
* implementar somente comportamentos especificados;
* utilizar Python 3.12+;
* utilizar type hints em funções e métodos;
* seguir princípios de Clean Code;
* seguir PEP 8;
* utilizar nomes descritivos;
* manter funções pequenas e coesas;
* aplicar Single Responsibility Principle quando apropriado;
* utilizar docstrings no estilo Google;
* utilizar tratamento específico de exceções;
* utilizar `TaskValidationError` para erros de validação;
* evitar divisão por zero;
* produzir mensagens de erro claras;
* manter o código compatível com os testes definidos no projeto.

---

## 4. Função pública obrigatória

A função pública principal deve manter o contrato:

```python
def analyze_tasks(tasks: list[dict]) -> dict:
    ...
```

A assinatura, o nome da função e seus parâmetros não devem ser alterados sem autorização explícita.

---

## 5. Validação

A implementação deve validar os dados de entrada conforme a especificação.

Entre as validações previstas estão:

* lista de tarefas vazia;
* campos obrigatórios ausentes;
* `id` inválido ou nulo;
* título vazio;
* prioridade inválida;
* status inválido;
* datas inválidas;
* `created_at` posterior a `due_date`;
* tarefa concluída sem `completed_at`;
* `completed_at` anterior a `created_at`;
* utilização de CPU fora do intervalo permitido.

Erros de validação devem utilizar exceções específicas e mensagens claras.

---

## 6. Métricas

As métricas devem seguir exatamente as regras estabelecidas na especificação.

Não devem ser criadas fórmulas, indicadores, limites ou comportamentos adicionais por iniciativa da IA.

Os campos de saída definidos na especificação devem ser preservados.

---

## 7. Testes

Os testes devem representar os cenários de aceitação definidos para o projeto.

A IA não deve:

* alterar testes apenas para fazer uma implementação incorreta passar;
* remover cenários de aceitação;
* ignorar erros identificados pelos testes;
* modificar o contrato para contornar uma falha.

Quando houver conflito entre implementação e teste, deve-se investigar a especificação antes de alterar qualquer componente.

---

## 8. Restrições

A IA NÃO deve:

* inventar requisitos;
* alterar requisitos arbitrariamente;
* criar funcionalidades não solicitadas;
* adicionar persistência de dados;
* adicionar bibliotecas não autorizadas ou desnecessárias;
* assumir comportamentos não especificados;
* ignorar validações;
* utilizar `except Exception: pass`;
* inserir credenciais, tokens ou segredos;
* alterar cenários de aceitação para favorecer a implementação;
* modificar a assinatura pública sem autorização;
* adicionar APIs ou serviços externos sem solicitação explícita.

---

## 9. Tratamento de ambiguidades

Quando houver informação insuficiente, ambiguidade ou conflito entre requisitos, a IA deve:

1. identificar explicitamente o problema;
2. apontar qual parte da especificação está envolvida;
3. não inventar uma regra silenciosamente;
4. solicitar decisão humana quando necessário.

---

## 10. Processo de desenvolvimento

O desenvolvimento deve seguir o fluxo:

**Especificação → Cenários de Aceitação → Implementação com IA → Test Harness → Execução dos Testes → Validação Humana → Commit**

A aprovação final da implementação é responsabilidade humana.

---

## 11. Princípio fundamental

> A IA é uma ferramenta de implementação e apoio técnico. A especificação é o contrato e a validação humana é a autoridade final.

Nenhuma sugestão gerada pela IA deve substituir os requisitos definidos para o projeto.
