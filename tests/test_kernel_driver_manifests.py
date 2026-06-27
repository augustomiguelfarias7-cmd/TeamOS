import tomllib
import unittest
from pathlib import Path


class KernelDriverManifestTest(unittest.TestCase):
    def test_kernel_manifest_points_to_linux_and_config_fragment(self):
        data = tomllib.loads(Path("kernel/linux.toml").read_text())

        self.assertIn("git.kernel.org", data["linux"]["repo"])
        self.assertEqual(data["linux"]["branch"], "linux-6.12.y")
        self.assertTrue(Path(data["teamos"]["config_fragment"]).exists())

    def test_driver_manifest_has_required_mobile_categories(self):
        data = tomllib.loads(Path("drivers/manifests/mobile.toml").read_text())
        driver_ids = {driver["id"] for driver in data["drivers"]}

        self.assertGreaterEqual(
            driver_ids,
            {"wifi", "display", "touch_input", "audio", "power"},
        )

    def test_custom_license_is_present(self):
        license_text = Path("LICENSE").read_text()

        self.assertIn("TeamOS Source License", license_text)
        self.assertIn("commercial", license_text)
        self.assertIn("malware", license_text)


if __name__ == "__main__":
    unittest.main()
