from foreightkillo import __version__
from foreightkillo.api import app


def test_public_namespace_and_product_identity() -> None:
    assert __version__ == "0.1.0"
    assert app.title == "For8killo"
