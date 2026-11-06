# CLAUDE.md

Entry point for Claude Code. Read and follow [AGENTS.md](AGENTS.md) in this same directory before working; it is the shared source of rules for both agents, including scope, branching, permissions, testing, and target-project adaptation.

AI-UnityPipeline itself is an instruction toolkit, not a Unity project. Do not run a Unity build here or change a Unity project elsewhere while maintaining this repository.

When installing these rules into a Unity project, copy both files and adapt the shared target-project guidance in `AGENTS.md`. Preserve existing Claude-specific instructions when integrating with a project that already has them.

Use the installed skill's `SKILL.md` for its workflow. In particular, `feature-cycle` includes functional verification and Performance & Reliability Code Review before temporary test cleanup and the final commit; `chat-notes` only saves a conversation summary.
