"""TeamOS Agent Mode guard.

The guard is the internal safety layer between ChatGusto and TeamOS system
features. It does not execute privileged actions directly. It reviews an access
request, produces warnings for the UI, and only creates a session after explicit
user approval.
"""

from __future__ import annotations

from dataclasses import dataclass

from .models import AgentModeRequest, AgentModeReview, AgentSession


@dataclass(frozen=True)
class AgentModePolicy:
    """Policy for Agent Mode requests."""

    trusted_origins: frozenset[str] = frozenset({"https://chatgusto-ai.genmb.com"})
    allowed_permissions: frozenset[str] = frozenset(
        {
            "open_url",
            "search_web",
            "open_settings",
            "read_current_page_title",
            "read_current_page_url",
            "read_battery_status",
            "read_wifi_status",
        }
    )


class AgentModeGuard:
    """Review and approve limited Agent Mode access."""

    def __init__(self, policy: AgentModePolicy | None = None) -> None:
        self.policy = policy or AgentModePolicy()

    def review_request(self, request: AgentModeRequest) -> AgentModeReview:
        """Review an Agent Mode request before showing a permission prompt."""

        normalized_origin = self._normalize_origin(request.origin)
        allowed_origin = normalized_origin in self.policy.trusted_origins
        approved_permissions = tuple(
            permission
            for permission in request.requested_permissions
            if permission in self.policy.allowed_permissions
        )
        denied_permissions = tuple(
            permission
            for permission in request.requested_permissions
            if permission not in self.policy.allowed_permissions
        )

        warnings: list[str] = []
        if not allowed_origin:
            warnings.append("Origem não confiável para o Modo Agente.")
        if denied_permissions:
            warnings.append("Algumas permissões solicitadas não são permitidas pelo TeamOS.")
        warnings.append(
            "Scanner e revisão reduzem riscos, mas não garantem segurança absoluta."
        )

        return AgentModeReview(
            request=AgentModeRequest(
                origin=normalized_origin,
                requested_permissions=request.requested_permissions,
                assistant_name=request.assistant_name,
            ),
            allowed_origin=allowed_origin,
            approved_permissions=approved_permissions,
            denied_permissions=denied_permissions,
            warnings=tuple(warnings),
        )

    def approve(self, review: AgentModeReview, user_confirmed: bool) -> AgentSession:
        """Create an Agent Mode session after explicit user confirmation."""

        if not user_confirmed:
            raise PermissionError("Usuário negou o Modo Agente.")
        if not review.can_prompt_user:
            raise PermissionError("Solicitação de Modo Agente reprovada na revisão.")

        return AgentSession(
            assistant_name=review.request.assistant_name,
            origin=review.request.origin,
            granted_permissions=review.approved_permissions,
        )

    def _normalize_origin(self, origin: str) -> str:
        """Normalize origin strings for comparison."""

        return origin.strip().rstrip("/")
