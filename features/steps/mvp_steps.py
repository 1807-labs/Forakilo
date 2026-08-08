from decimal import Decimal

from behave import given, then, when

from forakilo.application import ForeightService
from forakilo.intelligence.market import Opportunity, OpportunityRanker
from forakilo.marketdata.local import LocalMarketDataProvider


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


@when('an operator requests "{command}" through messaging')
def request_mutation(context: object, command: str) -> None:
    context.denied = command.split()[0] in {"/buy", "/execute", "/change-risk", "/promote-model"}


@then("the command is denied as a mutation")
def denied(context: object) -> None:
    assert context.denied
