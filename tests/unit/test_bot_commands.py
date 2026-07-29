from forakilo.bot.commands import parse_command


def test_parse_provider_qualified_command() -> None:
    command = parse_command("/signal@forakilo_bot abc-123", "command-1")
    assert command.name == "signal"
    assert command.arguments == ("abc-123",)
    assert command.command_id == "command-1"


def test_parse_command_rejects_empty_and_markup() -> None:
    for value in ("", "/bad<script>"):
        try:
            parse_command(value)
        except ValueError:
            pass
        else:
            raise AssertionError("invalid command was accepted")
