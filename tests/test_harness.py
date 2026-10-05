"""Test Harness for the Task Analyzer.

Tests the acceptance scenarios and edge cases defined in the SDD.
"""

import pytest

from src.task_analyzer import TaskValidationError, analyze_tasks


def build_task(
    task_id: int,
    priority: str,
    status: str,
    created_at: str,
    due_date: str,
    completed_at: str | None,
    cpu_usage_percent: float,
) -> dict:
    """Create a task fixture for the acceptance scenarios."""
    return {
        "id": task_id,
        "title": f"Tarefa {task_id}",
        "priority": priority,
        "created_at": created_at,
        "due_date": due_date,
        "completed_at": completed_at,
        "status": status,
        "cpu_usage_percent": cpu_usage_percent,
    }


def test_scenario_1_successful_analysis() -> None:
    """Validate the successful analysis acceptance scenario.

    The SDD defines five valid tasks:
    three completed on time, one completed late and one pending.
    """
    tasks = [
        build_task(
            1,
            "alta",
            "concluida",
            "2026-08-01T08:00:00",
            "2026-08-02T08:00:00",
            "2026-08-01T16:00:00",
            70.0,
        ),
        build_task(
            2,
            "alta",
            "concluida",
            "2026-08-01T09:00:00",
            "2026-08-03T09:00:00",
            "2026-08-02T09:00:00",
            75.0,
        ),
        build_task(
            3,
            "media",
            "concluida",
            "2026-08-02T08:00:00",
            "2026-08-03T08:00:00",
            "2026-08-02T12:00:00",
            80.0,
        ),
        build_task(
            4,
            "baixa",
            "concluida",
            "2026-08-02T10:00:00",
            "2026-08-03T10:00:00",
            "2026-08-04T16:00:00",
            85.0,
        ),
        build_task(
            5,
            "media",
            "pendente",
            "2026-08-03T08:00:00",
            "2026-08-05T08:00:00",
            None,
            70.0,
        ),
    ]

    result = analyze_tasks(tasks)

    # General metrics.
    assert result["total_tarefas_analisadas"] == 5
    assert result["total_tarefas_concluidas"] == 4
    assert result["total_tarefas_atrasadas"] == 1

    # Completion times:
    # 8h + 24h + 4h + 54h = 90h / 4 = 22.5h.
    assert result["tempo_medio_conclusao_horas"] == 22.5

    # One late task among four completed tasks.
    assert result["taxa_atraso_percentual"] == 25.0

    # Priority indicators.
    assert (
        result["indicadores_por_prioridade"]["alta"]["quantidade"]
        == 2
    )
    assert (
        result["indicadores_por_prioridade"]["alta"][
            "tempo_medio_conclusao_horas"
        ]
        == 16.0
    )
    assert (
        result["indicadores_por_prioridade"]["alta"][
            "taxa_atraso_percentual"
        ]
        == 0.0
    )

    assert (
        result["indicadores_por_prioridade"]["media"]["quantidade"]
        == 2
    )
    assert (
        result["indicadores_por_prioridade"]["media"][
            "tempo_medio_conclusao_horas"
        ]
        == 4.0
    )
    assert (
        result["indicadores_por_prioridade"]["media"][
            "taxa_atraso_percentual"
        ]
        == 0.0
    )

    assert (
        result["indicadores_por_prioridade"]["baixa"]["quantidade"]
        == 1
    )
    assert (
        result["indicadores_por_prioridade"]["baixa"][
            "tempo_medio_conclusao_horas"
        ]
        == 54.0
    )
    assert (
        result["indicadores_por_prioridade"]["baixa"][
            "taxa_atraso_percentual"
        ]
        == 100.0
    )

    # CPU average = (70 + 75 + 80 + 85 + 70) / 5 = 76%.
    assert result["recursos"]["cpu_media_percentual"] == 76.0
    assert result["recursos"]["alerta_cpu"] is False


def test_scenario_2_inconsistent_dates_raise_task_validation_error() -> None:
    """Validate rejection of a completion date before creation."""
    tasks = [
        build_task(
            1,
            "alta",
            "concluida",
            "2026-08-05T10:00:00",
            "2026-08-06T10:00:00",
            "2026-08-05T09:00:00",
            50.0,
        )
    ]

    with pytest.raises(TaskValidationError, match="completed_at"):
        analyze_tasks(tasks)


def test_scenario_3_empty_input_raises_value_error() -> None:
    """Validate rejection of an empty task list."""
    with pytest.raises(TaskValidationError, match="vazia"):
        analyze_tasks([])


def test_scenario_4_invalid_priority_raises_value_error() -> None:
    """Validate rejection of an invalid priority."""
    tasks = [
        build_task(
            1,
            "urgente",
            "pendente",
            "2026-08-01T08:00:00",
            "2026-08-02T08:00:00",
            None,
            50.0,
        )
    ]

    with pytest.raises(TaskValidationError, match="priority"):
        analyze_tasks(tasks)


def test_scenario_5_high_average_cpu_activates_alert() -> None:
    """Validate the CPU alert threshold defined by the SDD."""
    tasks = [
        build_task(
            1,
            "alta",
            "pendente",
            "2026-08-01T08:00:00",
            "2026-08-02T08:00:00",
            None,
            85.0,
        ),
        build_task(
            2,
            "media",
            "pendente",
            "2026-08-01T08:00:00",
            "2026-08-02T08:00:00",
            None,
            90.0,
        ),
    ]

    result = analyze_tasks(tasks)

    assert result["recursos"]["cpu_media_percentual"] == 87.5
    assert result["recursos"]["alerta_cpu"] is True


def test_pending_tasks_return_zero_delay_rate() -> None:
    """Validate metrics when there are no completed tasks."""
    tasks = [
        build_task(
            1,
            "alta",
            "pendente",
            "2026-08-01T08:00:00",
            "2026-08-02T08:00:00",
            None,
            30.0,
        ),
        build_task(
            2,
            "media",
            "em_andamento",
            "2026-08-01T08:00:00",
            "2026-08-03T08:00:00",
            None,
            40.0,
        ),
    ]

    result = analyze_tasks(tasks)

    assert result["total_tarefas_concluidas"] == 0
    assert result["total_tarefas_atrasadas"] == 0
    assert result["tempo_medio_conclusao_horas"] == 0.0
    assert result["taxa_atraso_percentual"] == 0.0
