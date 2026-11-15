# Status

This repository was extracted from the GPTAdmin source tree so the Chrome Profile Manager can evolve and be tested independently. The extraction source was the GPTAdmin main snapshot at fee2c656; the component remains experimental.

Confirmed in the retained QA evidence:

- isolated bridge protocol checks and temporary profile fixtures;
- profile discovery and fail-closed mutation logic;
- selected Linux and macOS disposable-profile scenarios.

Still unverified or deliberately limited:

- installation into an ordinary user profile;
- permanent chooser installation and independent readback after restart;
- Windows lifecycle operations;
- production GPTAdmin registration and consumer acceptance;
- modern MCP Tasks and subscriptions.

Historical GPTAdmin-dependent checks are kept under qa/gptadmin and are excluded from the default test path.
