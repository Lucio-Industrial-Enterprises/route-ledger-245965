import unittest

from warehouse.rates import shipping_quote


class RateTests(unittest.TestCase):
    def test_standard_rates(self):
        self.assertEqual(shipping_quote(2, "local"), 8.0)
        self.assertEqual(shipping_quote(2, "regional"), 11.0)

    def test_invalid_weight(self):
        for service in ("standard", "express"):
            for weight in (0, -1):
                with self.subTest(service=service, weight=weight):
                    with self.assertRaisesRegex(ValueError, "weight must be positive"):
                        shipping_quote(weight, "local", service)

    def test_explicit_standard_rates(self):
        for zone, expected in (("local", 8.0), ("regional", 11.0)):
            with self.subTest(zone=zone):
                self.assertEqual(shipping_quote(2, zone, service="standard"), expected)

    def test_express_rates(self):
        self.assertEqual(shipping_quote(2, "local", "express"), 15.0)
        self.assertEqual(shipping_quote(2, "regional", service="express"), 18.0)

    def test_express_surcharge_and_rounding(self):
        for zone in ("local", "regional"):
            for weight in (0.1, 1.234, 2, 10):
                with self.subTest(zone=zone, weight=weight):
                    standard = shipping_quote(weight, zone)
                    self.assertEqual(
                        standard, round((5.0 if zone == "local" else 8.0) + 1.5 * weight, 2)
                    )
                    self.assertEqual(
                        shipping_quote(weight, zone, "express"), round(standard + 7, 2)
                    )

    def test_invalid_zone(self):
        for service in ("standard", "express"):
            with self.subTest(service=service):
                with self.assertRaisesRegex(ValueError, "unknown zone"):
                    shipping_quote(2, "international", service)

    def test_invalid_service(self):
        for service in ("overnight", "", "Express", None):
            with self.subTest(service=service):
                with self.assertRaisesRegex(ValueError, "unknown service"):
                    shipping_quote(2, "local", service)
