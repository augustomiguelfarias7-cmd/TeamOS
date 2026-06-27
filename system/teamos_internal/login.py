"""TeamOS first-run login and local account setup.

TeamOS starts with an e-mail-only identity step, greets the user by a display
name derived from the e-mail, then requires a local PIN before opening the home
screen. This module stores the validation and state transition rules for that
flow; it does not store credentials or send network requests.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import re


class LoginStep(str, Enum):
    """Steps in the TeamOS first-run login flow."""

    EMAIL = "email"
    GREETING = "greeting"
    PIN = "pin"
    COMPLETE = "complete"


@dataclass(frozen=True)
class LoginIdentity:
    """Identity created from the user's e-mail address."""

    email: str
    display_name: str


@dataclass(frozen=True)
class PinPolicy:
    """Local TeamOS PIN rules."""

    min_length: int = 4
    max_length: int = 12
    digits_only: bool = True


@dataclass(frozen=True)
class LoginState:
    """Current first-run login state."""

    step: LoginStep = LoginStep.EMAIL
    identity: LoginIdentity | None = None
    pin_created: bool = False


class LoginFlow:
    """State machine for the TeamOS account creation flow."""

    _email_pattern = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

    def __init__(self, pin_policy: PinPolicy | None = None) -> None:
        self.pin_policy = pin_policy or PinPolicy()
        self.state = LoginState()

    def submit_email(self, email: str) -> LoginState:
        """Accept an e-mail address and advance to the greeting step."""

        normalized_email = email.strip().lower()
        if not self._email_pattern.match(normalized_email):
            raise ValueError("Digite um e-mail válido para entrar no TeamOS.")

        self.state = LoginState(
            step=LoginStep.GREETING,
            identity=LoginIdentity(
                email=normalized_email,
                display_name=self._display_name_from_email(normalized_email),
            ),
        )
        return self.state

    def continue_to_pin(self) -> LoginState:
        """Advance from greeting to PIN creation."""

        if self.state.step != LoginStep.GREETING or self.state.identity is None:
            raise RuntimeError("O TeamOS precisa validar o e-mail antes do PIN.")

        self.state = LoginState(step=LoginStep.PIN, identity=self.state.identity)
        return self.state

    def create_pin(self, pin: str, confirmation: str) -> LoginState:
        """Create a local PIN and complete the login flow."""

        if self.state.step != LoginStep.PIN or self.state.identity is None:
            raise RuntimeError("O PIN só pode ser criado depois da saudação.")
        self._validate_pin(pin, confirmation)

        self.state = LoginState(
            step=LoginStep.COMPLETE,
            identity=self.state.identity,
            pin_created=True,
        )
        return self.state

    def _validate_pin(self, pin: str, confirmation: str) -> None:
        if pin != confirmation:
            raise ValueError("Os PINs não são iguais.")
        if len(pin) < self.pin_policy.min_length:
            raise ValueError("O PIN é curto demais.")
        if len(pin) > self.pin_policy.max_length:
            raise ValueError("O PIN é longo demais.")
        if self.pin_policy.digits_only and not pin.isdigit():
            raise ValueError("O PIN deve conter apenas números.")

    def _display_name_from_email(self, email: str) -> str:
        local_part = email.split("@", maxsplit=1)[0]
        cleaned = re.sub(r"[._-]+", " ", local_part).strip()
        if not cleaned:
            return "usuário"
        return " ".join(part.capitalize() for part in cleaned.split())
