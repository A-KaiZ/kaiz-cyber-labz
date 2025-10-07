from __future__ import annotations

from pathlib import Path

import yaml


def test_victim_web_risky_disabled_by_default() -> None:
    compose = yaml.safe_load(Path("docker-compose.yml").read_text(encoding="utf-8"))
    env = compose["services"]["victim-web"]["environment"]
    assert "ENABLE_RISKY" in env
    assert "false" in env["ENABLE_RISKY"].lower()


def test_hardening_config_disables_password_auth() -> None:
    config = Path("blueteam/hardening/sshd_config.hard").read_text(encoding="utf-8")
    assert "PasswordAuthentication no" in config
    assert "AuthenticationMethods publickey" in config
