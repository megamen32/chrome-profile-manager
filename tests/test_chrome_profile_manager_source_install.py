"""Standalone source install and direct MCP child checks."""
import json
import os
from pathlib import Path
import subprocess
import sys
import stat

ROOT = Path(__file__).resolve().parents[1]

def install_command(prefix, state):
    return [sys.executable, str(ROOT / "install_chrome_profile_manager.py"),
            "--prefix", str(prefix), "--state-dir", str(state)]

def test_failed_install_can_be_retried_and_unsafe_state_is_rejected(tmp_path):
    prefix = tmp_path / "install"
    state = tmp_path / "state"
    command = install_command(prefix, state)
    env = os.environ.copy()
    env.update(PIP_NO_INDEX="1", PIP_NO_CACHE_DIR="1")
    failed = subprocess.run(command, env=env, capture_output=True, text=True)
    assert failed.returncode != 0
    assert not prefix.exists()
    state.chmod(0o755)
    rejected = subprocess.run(command, capture_output=True, text=True)
    assert rejected.returncode != 0
    assert not prefix.exists()
    assert stat.S_IMODE(state.stat().st_mode) == 0o755
    state.chmod(0o700)
    symlink = tmp_path / "state-link"
    symlink.symlink_to(state, target_is_directory=True)
    link_command = command[:-1] + [str(symlink)]
    assert subprocess.run(link_command, capture_output=True).returncode != 0
    assert not prefix.exists()
    subprocess.run(command, check=True, capture_output=True, text=True)
    assert prefix.is_dir()
    marker = prefix / "keep"
    marker.write_text("owned data")
    assert subprocess.run(command, capture_output=True).returncode != 0
    assert marker.read_text() == "owned data"

def test_source_install_and_direct_mcp_child(tmp_path):
    prefix = tmp_path / "installation with spaces"
    state = tmp_path / "state"
    result = subprocess.run(install_command(prefix, state), check=True, capture_output=True, text=True)
    registration = json.loads(result.stdout)
    assert stat.S_IMODE(state.stat().st_mode) == 0o700
    assert registration["config"]["ref"] == "chrome-profile-manager"
    assert (prefix / "chrome_profile_manager_bridge/host.py").is_file()
    assert (prefix / "chrome_profile_manager_bridge/extension/manifest.json").is_file()
    subprocess.run([str(prefix / "venv/bin/python"), "-c",
                    "import websocket, chrome_profile_helper; assert websocket.__version__ == '1.8.0'"],
                   cwd=prefix, check=True)

    roots = tmp_path / "empty-roots"
    roots.mkdir()
    env = os.environ.copy()
    env.update(CHROME_PROFILE_ROOTS=str(roots), CHROME_PROFILE_MANAGER_STATE=str(state))
    proc = subprocess.Popen([str(prefix / "venv/bin/python"), "-u",
                             str(prefix / "chrome_profile_manager_mcp.py")],
                            stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, text=True, env=env)
    try:
        request = {"jsonrpc": "2.0", "id": 1, "method": "tools/call",
                   "params": {"name": "profile_list", "arguments": {}}}
        proc.stdin.write(json.dumps(request) + "\n")
        proc.stdin.flush()
        response = json.loads(proc.stdout.readline())
        assert response["id"] == 1
        result = response["result"]["structuredContent"]
        assert result["profiles"] == []
    finally:
        proc.stdin.close()
        proc.wait(timeout=5)
