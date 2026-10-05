"""Task Analyzer implementation.

Implements the behavior defined in the SDD specification.
"""

from datetime import datetime
from statistics import mean
from typing import Any


class TaskValidationError(ValueError):
    """Raised when a task violates the SDD validation rules."""


VALID_PRIORITIES = {"alta", "media", "baixa"}
VALID_STATUSES = {"pendente", "em_andamento", "concluida"}
PRIORITIES = ("alta", "media", "baixa")


def _parse_date(value: str, field_name: str) -> datetime:
    """Parse an ISO 8601 date string."""
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (TypeError, ValueError) as exc:
        raise TaskValidationError(
            f"{field_name} deve ser uma data ISO 8601 válida."
        ) from exc


def _validate_task(task: dict[str, Any]) -> None:
    """Validate a single task according to the SDD rules."""
    required_fields = {
        "id",
        "title",
        "priority",
        "created_at",
        "due_date",
        "completed_at",
        "status",
    }

    missing_fields = required_fields - task.keys()
    if missing_fields:
        fields = ", ".join(sorted(missing_fields))
        raise TaskValidationError(
            f"Campos obrigatórios ausentes: {fields}."
        )

    if task["id"] is None or not isinstance(task["id"], (str, int)):
        raise TaskValidationError("id deve ser uma string ou inteiro não nulo.")

    if not isinstance(task["title"], str) or not task["title"].strip():
        raise TaskValidationError("title deve ser uma string não vazia.")

    if task["priority"] not in VALID_PRIORITIES:
        raise TaskValidationError(
            "priority deve ser 'alta', 'media' ou 'baixa'."
        )

    if task["status"] not in VALID_STATUSES:
        raise TaskValidationError(
            "status deve ser 'pendente', 'em_andamento' ou 'concluida'."
        )

    created_at = _parse_date(task["created_at"], "created_at")
    due_date = _parse_date(task["due_date"], "due_date")

    if created_at > due_date:
        raise TaskValidationError(
            "created_at não pode ser posterior a due_date."
        )

    completed_at_value = task["completed_at"]

    if task["status"] == "concluida" and completed_at_value is None:
        raise TaskValidationError(
            "Tarefas concluídas devem possuir completed_at."
        )

    completed_at = None
    if completed_at_value is not None:
        completed_at = _parse_date(completed_at_value, "completed_at")

        if completed_at < created_at:
            raise TaskValidationError(
                "completed_at não pode ser anterior a created_at."
            )

    cpu_usage = task.get("cpu_usage_percent")

    if cpu_usage is not None:
        if not isinstance(cpu_usage, (int, float)) or isinstance(cpu_usage, bool):
            raise TaskValidationError(
                "cpu_usage_percent deve ser numérico."
            )

        if not 0 <= cpu_usage <= 100:
            raise TaskValidationError(
                "cpu_usage_percent deve estar entre 0 e 100."
            )


def _completion_time_hours(task: dict[str, Any]) -> float | None:
    """Calculate completion time in hours for a completed task."""
    if task["completed_at"] is None:
        return None

    created_at = _parse_date(task["created_at"], "created_at")
    completed_at = _parse_date(task["completed_at"], "completed_at")

    return (completed_at - created_at).total_seconds() / 3600


def _is_delayed(task: dict[str, Any]) -> bool:
    """Return whether a completed task was completed after its due date."""
    if task["completed_at"] is None:
        return False

    completed_at = _parse_date(task["completed_at"], "completed_at")
    due_date = _parse_date(task["due_date"], "due_date")

    return completed_at > due_date


def _calculate_group_metrics(
    tasks: list[dict[str, Any]],
) -> dict[str, float | int]:
    """Calculate completion and delay metrics for a group of tasks."""
    completed_tasks = [
        task for task in tasks if task["status"] == "concluida"
    ]

    completion_times = [
        completion_time
        for task in completed_tasks
        if (completion_time := _completion_time_hours(task)) is not None
    ]

    delayed_tasks = [
        task for task in completed_tasks if _is_delayed(task)
    ]

    average_completion = (
        round(mean(completion_times), 2)
        if completion_times
        else 0.0
    )

    delay_rate = (
        round(len(delayed_tasks) / len(completed_tasks) * 100, 2)
        if completed_tasks
        else 0.0
    )

    return {
        "quantidade": len(tasks),
        "tempo_medio_conclusao_horas": average_completion,
        "taxa_atraso_percentual": delay_rate,
    }


def _calculate_resource_metrics(
    tasks: list[dict[str, Any]],
) -> dict[str, float | bool | None]:
    """Calculate CPU resource metrics."""
    cpu_values = [
        task["cpu_usage_percent"]
        for task in tasks
        if task.get("cpu_usage_percent") is not None
    ]

    if not cpu_values:
        return {
            "media_cpu_percent": None,
            "alerta_cpu": False,
        }

    average_cpu = round(mean(cpu_values), 2)

    return {
        "media_cpu_percent": average_cpu,
        "alerta_cpu": average_cpu >= 80,
    }


def analyze_tasks(tasks: list[dict[str, Any]]) -> dict[str, Any]:
    """Analyze tasks and return productivity metrics.

    Args:
        tasks: List of task dictionaries defined by the SDD.

    Returns:
        Dictionary containing general, priority and resource metrics.

    Raises:
        TaskValidationError: If the input or any task violates the SDD.
    """
    if not isinstance(tasks, list) or not tasks:
        raise TaskValidationError("A lista de tarefas não pode ser vazia.")

    for task in tasks:
        if not isinstance(task, dict):
            raise TaskValidationError("Cada tarefa deve ser um dicionário.")
        _validate_task(task)

    completed_tasks = [
        task for task in tasks if task["status"] == "concluida"
    ]

    delayed_tasks = [
        task for task in completed_tasks if _is_delayed(task)
    ]

    completion_times = [
        completion_time
        for task in completed_tasks
        if (completion_time := _completion_time_hours(task)) is not None
    ]

    average_completion = (
        round(mean(completion_times), 2)
        if completion_times
        else 0.0
    )

    delay_rate = (
        round(len(delayed_tasks) / len(completed_tasks) * 100, 2)
        if completed_tasks
        else 0.0
    )

    indicators_by_priority = {}

    for priority in PRIORITIES:
        priority_tasks = [
            task for task in tasks if task["priority"] == priority
        ]
        indicators_by_priority[priority] = _calculate_group_metrics(
            priority_tasks
        )

    return {
        "tempo_medio_conclusao_horas": average_completion,
        "taxa_atraso_percentual": delay_rate,
        "total_tarefas_analisadas": len(tasks),
        "total_tarefas_concluidas": len(completed_tasks),
        "total_tarefas_atrasadas": len(delayed_tasks),
        "indicadores_por_prioridade": indicators_by_priority,
        "recursos": _calculate_resource_metrics(tasks),
    }
