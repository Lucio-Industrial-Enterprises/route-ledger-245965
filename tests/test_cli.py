import subprocess
import sys
import unittest
from pathlib import Path


class CliTests(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run(
            [sys.executable, "-m", "warehouse.cli", *args],
            cwd=Path(__file__).resolve().parents[1],
            capture_output=True,
            text=True,
        )

    def test_default_standard_quotes(self):
        for zone, expected in (("local", "$8.00
"), ("regional", "$11.00
")):
            with self.subTest(zone=zone):
                result = self.run_cli("2", zone)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(result.stdout, expected)

    def test_explicit_standard_quote(self):
        result = self.run_cli("2", "local", "--service", "standard")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "$8.00
")

    def test_express_quotes(self):
        for zone, expected in (("local", "$15.00
"), ("regional", "$18.00
")):
            with self.subTest(zone=zone):
                result = self.run_cli("2", zone, "--service", "express")
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(result.stdout, expected)

    def test_invalid_service(self):
        result = self.run_cli("2", "local", "--service", "overnight")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertIn("invalid choice", result.stderr)

    def test_help_lists_services(self):
        result = self.run_cli("--help")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("--service {standard,express}", result.stdout)
