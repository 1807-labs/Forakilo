# Bot command reference

The bot surface is read-only. It cannot place, modify, approve, or cancel orders.

| Command | Result |
| --- | --- |
| `/help` | List the supported read-only commands. |
| `/status`, `/health` | Show known component health. |
| `/signals` | List recent signal projections. |
| `/signal <id>` | Show one signal projection. |
| `/risk` | Show current risk status. |
| `/paper` | Show the paper account summary. |
| `/positions` | List paper positions. |
| `/strategies` | List strategy versions. |
| `/strategy <id>` | Show one strategy summary. |
| `/performance <id>` | Show strategy performance when available. |
| `/models` | List known model versions. |

Unavailable data returns `NOT_AVAILABLE`; the gateway does not invent a value. Unknown,
mutating, or unauthorized commands fail closed and create a redacted audit record.
