# Warehouse tools

Small Python utilities for warehouse order and shipping workflows.

Run the tests with `python3 -m unittest discover -s tests -v`.

## Shipping

`shipping_quote(weight_kg, zone, service="standard")` returns a delivery quote in
dollars, rounded to two decimal places. Zones are `local` and `regional`; weights
must be positive. Standard shipping remains the default and costs $5 for local
or $8 for regional, plus $1.50 per kilogram. Express shipping adds $7 to the
standard quote in either zone. Unknown zones or services and non-positive weights
raise `ValueError`.

```python
from warehouse.rates import shipping_quote

shipping_quote(2, "local")                     # 8.0 (standard, unchanged)
shipping_quote(2, "local", service="express")  # 15.0
shipping_quote(2, "regional", "express")       # 18.0
```

Run the command-line entry point from the repository root. It prints the quote
with two decimal places; `--service` accepts `standard` (the default) or `express`.
Unknown services are rejected.

```sh
python3 -m warehouse.cli 2 local                    # $8.00
python3 -m warehouse.cli 2 local --service standard # $8.00
python3 -m warehouse.cli 2 local --service express  # $15.00
python3 -m warehouse.cli 2 regional --service express # $18.00
```
