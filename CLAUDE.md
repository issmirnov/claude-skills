# claude-skills

Public repository of Claude plugins by Smirnov Labs, published to Anthropic's plugin directory. The repository root is a plugin marketplace named `smirnov-labs` (`.claude-plugin/marketplace.json`). Each folder under `plugins/` is one plugin and one directory submission, with plugin path `plugins/<name>`.

## Add a plugin

1. Create `plugins/<name>/` with these files:
   - `.claude-plugin/plugin.json` with `name`, `displayName`, `version`, `description`, `author` (`Smirnov Labs`), `license` (`MIT`), `keywords` and `icon` (`./icon.png`). Nothing else goes in `.claude-plugin/`.
   - `icon.png` at the plugin root.
   - `README.md` of at least 40 words outside code blocks, covering what the plugin does, how to use it and what data it sends. The directory shows it as the listing description.
   - `LICENSE`.
   - `skills/<skill>/SKILL.md`, where the folder name matches the skill's `name`. Put its `description` in double quotes: the directory's YAML parser flags an unquoted value that contains a colon followed by a space.
   - Any code the skill runs, in `skills/<skill>/scripts/`, called as `python3 ${CLAUDE_SKILL_DIR}/scripts/<file>`. The directory flags a download piped into an interpreter, such as `curl ... | python3`, as download-and-execute.
2. Add the plugin to `.claude-plugin/marketplace.json` with `"source": "./plugins/<name>"`.
3. Add a row to the table in `README.md`. Its button links to `https://claude.ai/customize/plugins/new?marketplace=issmirnov/claude-skills&plugin=<name>`.
4. Run `claude plugin validate .` and `claude plugin validate --profile directory --strict ./plugins/<name>`.
5. Run `detect-secrets scan` and read the added lines for client names, internal hosts, private IPs and home paths, since the repository is public.

Keep these out of each plugin folder: a `bin/` directory, symlinks, zips and binaries other than images. claude.ai won't install a plugin that has a `bin/` directory. Raise `version` in `plugin.json` with every change to a published plugin.

## Submit to the directory

At claude.ai/directory/manage, choose **Submit new**, then **Plugin bundle**. Enter repository `issmirnov/claude-skills` and plugin path `plugins/<name>`, select **Validate** and fix every finding marked Blocking. After the directory lists a plugin, it scans each new commit on `main`. A version that passes goes live when you select **Publish** on the plugin's page, unless auto-publish is on.
