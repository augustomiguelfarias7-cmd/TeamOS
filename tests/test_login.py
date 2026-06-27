import unittest

from system.teamos_internal.login import LoginFlow, LoginStep


class LoginFlowTest(unittest.TestCase):
    def test_email_creates_greeting_name(self):
        flow = LoginFlow()

        state = flow.submit_email("mano.team-os@example.com")

        self.assertEqual(state.step, LoginStep.GREETING)
        self.assertEqual(state.identity.email, "mano.team-os@example.com")
        self.assertEqual(state.identity.display_name, "Mano Team Os")

    def test_invalid_email_is_rejected(self):
        flow = LoginFlow()

        with self.assertRaises(ValueError):
            flow.submit_email("sem-arroba")

    def test_pin_completes_login_flow(self):
        flow = LoginFlow()

        flow.submit_email("user@example.com")
        pin_state = flow.continue_to_pin()
        complete_state = flow.create_pin("1234", "1234")

        self.assertEqual(pin_state.step, LoginStep.PIN)
        self.assertEqual(complete_state.step, LoginStep.COMPLETE)
        self.assertTrue(complete_state.pin_created)

    def test_pin_must_match(self):
        flow = LoginFlow()
        flow.submit_email("user@example.com")
        flow.continue_to_pin()

        with self.assertRaises(ValueError):
            flow.create_pin("1234", "4321")


if __name__ == "__main__":
    unittest.main()
