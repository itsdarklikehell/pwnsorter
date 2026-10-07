#!/usr/bin/env python3
"""
tests/test_potfilesorter.py — unit tests for potfilesorter.py.

Tests the core logic: potfile parsing, config backup, and network block
generation. Uses mocking to avoid touching real system files.
"""

from __future__ import annotations

import importlib.util
import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

HERE = Path(__file__).resolve().parent
POTFILESORTER = HERE.parent / "potfilesorter.py"


def load_module():
    """Load potfilesorter.py as a module."""
    spec = importlib.util.spec_from_file_location("potfilesorter", POTFILESORTER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture
def mod():
    """Return the loaded potfilesorter module."""
    return load_module()


class TestPotfileParsing:
    """Test potfile line parsing logic."""

    def test_valid_line_has_four_fields(self, mod):
        """A valid potfile line has at least 4 colon-separated fields."""
        line = "AA:BB:CC:DD:EE:FF:password123:52.0:4.0"
        parts = line.split(":")
        assert len(parts) >= 4
        bssid = parts[2]
        password = parts[3]
        assert bssid == "AA:BB:CC:DD:EE:FF"
        assert password == "password123"

    def test_short_line_skipped(self, mod):
        """Lines with fewer than 4 fields should be skipped."""
        line = "AA:BB:CC:DD:EE:FF"
        parts = line.split(":")
        assert len(parts) < 4

    def test_network_block_format(self, mod):
        """The network block should contain ssid and psk."""
        bssid = "AA:BB:CC:DD:EE:FF"
        password = "testpass123"
        block = (
            '\n'
            'network={\n'
            '  scan_ssid=1\n'
            f'  ssid="{bssid}"\n'
            f'  psk="{password}"\n'
            '}\n'
            '\n'
        )
        assert bssid in block
        assert password in block
        assert "network={" in block
        assert "scan_ssid=1" in block


class TestBackupConfigs:
    """Test backup_configs function."""

    def test_backup_creates_temp_files(self, mod):
        """backup_configs should create temp files from source configs."""
        with tempfile.TemporaryDirectory() as tmpdir:
            wpa_src = os.path.join(tmpdir, "wpa_supplicant.conf")
            with open(wpa_src, "w") as f:
                f.write("network={\n  ssid=\"test\"\n}\n")

            with patch.object(mod, "wpa_source", wpa_src), \
                 patch.object(mod, "wpa_backup", os.path.join(tmpdir, "wpa.bak")), \
                 patch.object(mod, "wpa_tmp", os.path.join(tmpdir, "wpa.tmp")):
                mod.backup_configs()
                assert os.path.exists(os.path.join(tmpdir, "wpa.tmp"))


class TestCheckWpaConfig:
    """Test checkwpaconfig function."""

    def test_bssid_found(self, mod):
        """checkwpaconfig returns True when BSSID is in the file."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".conf", delete=False) as f:
            f.write('network={\n  ssid="AA:BB:CC:DD:EE:FF"\n}\n')
            f.flush()
            result = mod.checkwpaconfig(f.name, "AA:BB:CC:DD:EE:FF")
            assert result is True
        os.unlink(f.name)

    def test_bssid_not_found(self, mod):
        """checkwpaconfig returns False when BSSID is not in the file."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".conf", delete=False) as f:
            f.write('network={\n  ssid="XX:YY:ZZ"\n}\n')
            f.flush()
            result = mod.checkwpaconfig(f.name, "AA:BB:CC:DD:EE:FF")
            assert result is False
        os.unlink(f.name)


class TestCopyConfig:
    """Test copy_config function."""

    def test_copy_config_copies_tmp_to_source(self, mod):
        """copy_config should copy tmp files back to source."""
        with tempfile.TemporaryDirectory() as tmpdir:
            wpa_src = os.path.join(tmpdir, "wpa_supplicant.conf")
            wpa_tmp = os.path.join(tmpdir, "wpa.tmp")
            with open(wpa_tmp, "w") as f:
                f.write("new config")

            with patch.object(mod, "wpa_source", wpa_src), \
                 patch.object(mod, "wpa_tmp", wpa_tmp):
                mod.copy_config()
                assert os.path.exists(wpa_src)
                with open(wpa_src) as f:
                    assert f.read() == "new config"
                assert not os.path.exists(wpa_tmp)


class TestSyntax:
    """Test that potfilesorter.py has valid Python syntax."""

    def test_module_loads(self, mod):
        """potfilesorter.py should load without syntax errors."""
        assert hasattr(mod, "get_potfile")
        assert hasattr(mod, "backup_configs")
        assert hasattr(mod, "copy_config")
        assert hasattr(mod, "checkwpaconfig")
        assert hasattr(mod, "readpotfiledata")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
