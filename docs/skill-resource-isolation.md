# Skill resources and cross-runtime parity

The canonical Skill model distinguishes **missing** resource fields from explicit
empty lists. An omitted `references`, `assets` or `scripts` uses the legacy
project-level fallback; an explicit `[]` disables that resource class for the
Skill. Nonempty declarations select only those files. This rule applies to the
Plugin and Claude Skills resource resolvers, without changing the complete
instruction projection used by Chat ZIP or Claude Projects.

Use `requires_skills` to declare dependencies between Skill workflows. Entries
must refer to a declared Skill ID, cannot refer to the Skill itself, and cannot
form cycles. Generated `SKILL.md` files describe the handoff and instruct the
runtime not to assume the other Skill's files exist under the current Skill.
Handoff is instructional, not a guarantee that the host can activate a Skill.

GPT Byggaren declares `scripts: []` on project workflow and legacy analysis.
Only distribution-and-parity inherits the declared runtime script tools and
has the Work-oriented, file-executable canonical engine resources in Plugin.
Claude Skills preserves its existing engine packaging. No MCP wrapper is added.

Run `python -m pytest tests/test_skill_distribution_parity.py
tests/test_plugin_distribution.py tests/test_split_claude_distributions.py`
and the full test suite before merging. Structural checks are not equivalent
to live execution in ChatGPT Work, Claude or OpenCode.
