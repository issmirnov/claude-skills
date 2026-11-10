# Smirnov Labs skills for Claude

Skills for Claude, packaged as plugins. Each plugin under [`plugins/`](plugins/) works on claude.ai, in the desktop app and Cowork, and in Claude Code. The plugins follow the layout of Anthropic's plugin directory. Until the directory lists a plugin, use its button below to add it from this repository.

| Plugin | What it does | Add it |
| --- | --- | --- |
| [SMART Goals Coach](plugins/smart-goals-coach/) | Turns a fuzzy wish into one to three goals you can start this week, with a goal card, a first step and an if-then plan. | [![Add SMART Goals Coach to Claude](https://img.shields.io/badge/Add_to_Claude-B05730?style=for-the-badge)](https://claude.ai/customize/plugins/new?marketplace=issmirnov/claude-skills&plugin=smart-goals-coach) |

## Add a plugin on claude.ai or the desktop app

1. Select the plugin's **Add to Claude** button.
2. If Claude asks you to sign in, sign in.
3. Confirm adding this repository's marketplace and the plugin. The button fills in both.

If the button doesn't open that view, add the marketplace yourself:

1. Open **Plugins** in Claude's sidebar. If your sidebar shows **Customize** instead, open **Customize > Plugins**.
2. Select **Add > Add marketplace**, enter `issmirnov/claude-skills` and confirm.
3. Add the plugin from the marketplace's list.

Plugins need a Pro, Max, Ultra, Team or Enterprise plan. Turn on **Code execution and file creation** in **Settings > Capabilities**. On Team and Enterprise plans, an Owner decides whether members can add marketplaces.

## Add a plugin in Claude Code

```
/plugin marketplace add issmirnov/claude-skills
/plugin install smart-goals-coach@smirnov-labs
```

## Data

Each plugin's README says what it sends and stores. SMART Goals Coach is instructions only: it has no connectors or scripts and sends nothing to any outside service.

## License

MIT. See [LICENSE](LICENSE).
