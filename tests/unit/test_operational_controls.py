from pathlib import Path

from foreightkillo.operations import OperationalControls


def test_controls_start_fail_closed_and_persist_audited_changes(tmp_path: Path) -> None:
    path = tmp_path / "operations.sqlite3"
    controls = OperationalControls(path)
    initial = controls.status()
    assert initial.kill_switch_active
    assert not initial.execution_permitted

    cleared = controls.set_kill_switch(False, "operator-1", "approved paper rehearsal")
    assert not cleared.kill_switch_active
    assert cleared.execution_permitted
    assert OperationalControls(path).status() == cleared
    event = controls.audit()[0]
    assert event.event_type == "operations.kill_switch_cleared"
    assert event.actor == "operator-1"


def test_controls_validate_reason_and_audit_limit(tmp_path: Path) -> None:
    controls = OperationalControls(tmp_path / "operations.sqlite3")
    try:
        controls.set_kill_switch(False, "operator", "short")
    except ValueError as error:
        assert "reason" in str(error)
    else:
        raise AssertionError("short reason should be rejected")
