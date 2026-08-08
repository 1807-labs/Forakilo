# ruff: noqa: E501
"""Small dependency-free operator dashboard for the self-hosted MVP."""

DASHBOARD_HTML = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width">
<title>For8killo - Foreight</title><style>
body{font:16px system-ui;background:#08111f;color:#dbeafe;margin:0}main{max-width:1100px;margin:auto;padding:2rem}
h1{color:#67e8f9}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:1rem}
section{background:#111c2f;border:1px solid #263854;border-radius:12px;padding:1rem}code{color:#fde68a}
.safe{color:#86efac}.warn{color:#fca5a5}</style></head><body><main>
<h1>For8killo <small>Foreight</small></h1><p class="safe">PAPER MODE - intelligence before execution.</p>
<div class="grid"><section><h2>Market intelligence</h2><p>Explainable structure, liquidity, regime and volatility.</p></section>
<section><h2>Risk boundary</h2><p>Signals cannot become orders without deterministic risk and authorization.</p></section>
<section><h2>API</h2><p>Use <code>/docs</code> for authenticated operations.</p></section></div>
<p class="warn">Market research only. No returns are guaranteed. Live-money execution is disabled.</p>
</main></body></html>"""
