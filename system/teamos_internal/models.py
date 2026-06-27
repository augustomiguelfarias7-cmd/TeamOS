"""Shared data models for TeamOS internal services."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass(frozen=True)
class AgentModeRequest:
    """A website or assistant request to become a TeamOS agent."""

    origin: str
    requested_permissions: tuple[str, ...]
    assistant_name: str = "ChatGusto"


@dataclass(frozen=True)
class AgentModeReview:
    """Security review result that can be shown before the permission prompt."""

    request: AgentModeRequest
    allowed_origin: bool
    approved_permissions: tuple[str, ...]
    denied_permissions: tuple[str, ...]
    warnings: tuple[str, ...] = ()

    @property
    def can_prompt_user(self) -> bool:
        """Return whether TeamOS may show the final user permission prompt."""

        return self.allowed_origin and not self.denied_permissions


@dataclass(frozen=True)
class AgentSession:
    """An approved Agent Mode session."""

    assistant_name: str
    origin: str
    granted_permissions: tuple[str, ...]
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass(frozen=True)
class WifiNetwork:
    """A Wi-Fi network reported by Linux NetworkManager."""

    ssid: str
    signal: int
    security: str
    active: bool = False
