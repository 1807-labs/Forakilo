from datetime import UTC, datetime, timedelta
from decimal import Decimal
from pathlib import Path
from tempfile import TemporaryDirectory

from behave import given, then, when

from foreightkillo.application import ForeightService
from foreightkillo.brokers.local import LocalBroker
from foreightkillo.domain import EventIdentity, InstrumentId, OrderProposal, Side
from foreightkillo.execution import Authorization, PracticeExecutionService
from foreightkillo.intelligence import (
    ForeightConversation,
    ResearchRepository,
    SQLiteConversationMemory,
)
from foreightkillo.intelligence.market import Opportunity, OpportunityRanker
from foreightkillo.marketdata.local import LocalMarketDataProvider
from foreightkillo.operations import OperationalControls
from foreightkillo.queries import QueryService
from foreightkillo.risk import RiskDecision, RiskOutcome


@when('Foreight analyzes "{instrument}"')
def analyze(context: object, instrument: str) -> None:
    try:
        context.result = ForeightService(LocalMarketDataProvider()).analyze(instrument)
        context.error = None
    except KeyError as error:
        context.error = error


@then('the result identifies "{market}"')
def identifies_market(context: object, market: str) -> None:
    assert context.result["asset_class"] == market


@then("the result is explainable and paper-only")
def explainable(context: object) -> None:
    assert context.result["reasons"] and context.result["paper_only"] is True


@then("the instrument is reported as unsupported")
def unsupported(context: object) -> None:
    assert isinstance(context.error, KeyError)


@given("eligible opportunities with costs and exposure penalties")
def opportunities(context: object) -> None:
    context.opportunities = (
        Opportunity(
            "gold",
            Decimal("0.6"),
            Decimal("2.8"),
            Decimal("0.1"),
            Decimal("1"),
            Decimal("1"),
            Decimal("0.1"),
            Decimal("0.1"),
        ),
        Opportunity(
            "crypto",
            Decimal("0.3"),
            Decimal("1.9"),
            Decimal("0.2"),
            Decimal("0.8"),
            Decimal("0.5"),
            Decimal("0.2"),
            Decimal("0.2"),
        ),
    )


@when("Foreight ranks the opportunities")
def rank(context: object) -> None:
    context.ranked = OpportunityRanker().rank(context.opportunities)


@then("the strongest net opportunity is ranked first")
def strongest(context: object) -> None:
    assert context.ranked[0].signal_id == "gold"


@when('Foreight researches strategies for "{instrument}"')
def research_strategies(context: object, instrument: str) -> None:
    context.strategy_research = ForeightService(LocalMarketDataProvider(seed=8)).strategy_research(
        instrument
    )


@then("the research covers the configured strategy families")
def covers_strategy_families(context: object) -> None:
    assert {item["strategy"] for item in context.strategy_research["candidates"]} == {
        "trend-following",
        "momentum",
        "volatility-breakout",
        "mean-reversion",
        "harmonic",
    }


@then("the research compares three timeframes")
def compares_timeframes(context: object) -> None:
    assert len(context.strategy_research["multi_timeframe"]["timeframes"]) == 3


@then("the research has no execution authority")
def has_no_execution_authority(context: object) -> None:
    assert context.strategy_research["execution_authority"] is False


@given("a new For8killo installation")
def new_installation(context: object) -> None:
    context.temporary_directory = TemporaryDirectory(ignore_cleanup_errors=True)
    context.controls = OperationalControls(Path(context.temporary_directory.name) / "state.sqlite3")


@when("the operator checks operational status")
def check_operational_status(context: object) -> None:
    context.operational_status = context.controls.status()


@then("the kill switch is active")
def kill_switch_active(context: object) -> None:
    assert context.operational_status.kill_switch_active


@then("execution is not permitted")
def execution_not_permitted(context: object) -> None:
    assert not context.operational_status.execution_permitted
    context.temporary_directory.cleanup()


@when('an operator asks Foreight to "{question}"')
def ask_foreight(context: object, question: str) -> None:
    context.conversation_directory = TemporaryDirectory(ignore_cleanup_errors=True)
    conversation = ForeightConversation(
        QueryService(),
        ResearchRepository(),
        SQLiteConversationMemory(
            Path(context.conversation_directory.name) / "conversation.sqlite3"
        ),
    )
    context.conversation_response = conversation.ask("behavior", question)


@then("Foreight refuses conversational execution")
def refuses_conversational_execution(context: object) -> None:
    assert "cannot authorize or execute" in context.conversation_response.text
    context.conversation_directory.cleanup()


@given("an authorized practice proposal with rejected risk")
def rejected_practice_proposal(context: object) -> None:
    now = datetime(2026, 8, 8, tzinfo=UTC)
    identity = EventIdentity("proposal", now, now, now, "behavior", "run", None, "1")
    proposal = OrderProposal(
        identity,
        "signal",
        InstrumentId("local", "EUR_USD"),
        Side.BUY,
        Decimal("10"),
        Decimal("1.10"),
        Decimal("1.09"),
        now + timedelta(minutes=5),
        "sandbox-manual",
    )
    context.practice_now = now
    context.practice_proposal = proposal
    context.practice_decision = RiskDecision(
        RiskOutcome.REJECTED, ("risk_limit",), proposal.proposal_hash
    )
    context.practice_authorization = Authorization(
        "authorization", proposal.proposal_hash, "operator", now + timedelta(minutes=2)
    )


@when("the practice proposal is submitted")
def submit_practice_proposal(context: object) -> None:
    try:
        PracticeExecutionService(LocalBroker()).submit(
            context.practice_proposal,
            context.practice_decision,
            context.practice_authorization,
            context.practice_now,
        )
        context.practice_denied = False
    except PermissionError:
        context.practice_denied = True


@then("practice execution is denied")
def practice_execution_denied(context: object) -> None:
    assert context.practice_denied


@when('an operator requests "{command}" through messaging')
def request_mutation(context: object, command: str) -> None:
    context.denied = command.split()[0] in {"/buy", "/execute", "/change-risk", "/promote-model"}


@then("the command is denied as a mutation")
def denied(context: object) -> None:
    assert context.denied
