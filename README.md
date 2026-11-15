# Chrome Profile Manager

An experimental MCP server and native messaging bridge for inspecting and managing unpacked Chrome extensions in an explicitly paired profile. It is a standalone candidate component for MCP hosts; it is not part of GPTAdmin core.

The project currently supports profile discovery and a profile-scoped extension bridge on Linux and macOS test setups. Ordinary user profiles, Windows lifecycle operations, permanent chooser installation, and modern MCP Tasks/subscriptions remain limited or unverified. Read the capability and limitation notes in docs/CHROME_PROFILE_MANAGER_MCP.md before use.

## Install

From a checkout with Python 3 and network access for the pinned wheel:

    python3 install_chrome_profile_manager.py \
      --prefix "$HOME/.local/lib/chrome-profile-manager-1" \
      --state-dir "$HOME/.local/state/chrome-profile-manager"

The command creates a private installation and prints an MCP registration object. Add that object to the MCP host you operate, then configure a disposable Chrome profile with the bridge provisioner. Installation does not open, copy, or modify an existing browser profile.

## Check the source

    python3 -m pip install -r chrome_profile_manager_requirements.txt pytest
    python3 -m pytest

The normal test suite uses temporary state and does not require a real Chrome profile. Real browser checks are opt-in and documented separately. The qa/gptadmin directory preserves historical checks that require a private GPTAdmin or ShellMCP installation.

## Documentation

- MCP capabilities, setup, and limitations: docs/CHROME_PROFILE_MANAGER_MCP.md
- Bridge protocol and profile binding: chrome_profile_manager_bridge/README.md
- Current experimental status: docs/STATUS.md
- Archived QA evidence: chrome_profile_manager_bridge/QA_EVIDENCE.md

## License

AGPL-3.0-or-later; see LICENSE.
