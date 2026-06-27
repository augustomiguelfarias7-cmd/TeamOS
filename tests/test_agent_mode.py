import unittest

from system.teamos_internal import AgentModeGuard, AgentModeRequest


class AgentModeGuardTest(unittest.TestCase):
    def test_trusted_chatgusto_request_can_prompt_user(self):
        guard = AgentModeGuard()
        request = AgentModeRequest(
            origin="https://chatgusto-ai.genmb.com/",
            requested_permissions=("open_url", "search_web", "read_wifi_status"),
        )

        review = guard.review_request(request)

        self.assertTrue(review.allowed_origin)
        self.assertTrue(review.can_prompt_user)
        self.assertEqual(review.denied_permissions, ())

    def test_unknown_origin_is_rejected(self):
        guard = AgentModeGuard()
        request = AgentModeRequest(
            origin="https://fake-chatgusto.example",
            requested_permissions=("open_url",),
        )

        review = guard.review_request(request)

        self.assertFalse(review.allowed_origin)
        self.assertFalse(review.can_prompt_user)

    def test_denied_permission_blocks_prompt(self):
        guard = AgentModeGuard()
        request = AgentModeRequest(
            origin="https://chatgusto-ai.genmb.com",
            requested_permissions=("open_url", "delete_files"),
        )

        review = guard.review_request(request)

        self.assertEqual(review.approved_permissions, ("open_url",))
        self.assertEqual(review.denied_permissions, ("delete_files",))
        self.assertFalse(review.can_prompt_user)

    def test_approval_requires_user_confirmation(self):
        guard = AgentModeGuard()
        review = guard.review_request(
            AgentModeRequest(
                origin="https://chatgusto-ai.genmb.com",
                requested_permissions=("open_settings",),
            )
        )

        with self.assertRaises(PermissionError):
            guard.approve(review, user_confirmed=False)

        session = guard.approve(review, user_confirmed=True)
        self.assertEqual(session.granted_permissions, ("open_settings",))


if __name__ == "__main__":
    unittest.main()
