# 🔒 Clawdbot Core Skills — READ-ONLY REFERENCE

These are Clawdbot's built-in system skills. They are stored here as REFERENCES ONLY.

**⚠️ NEVER modify the originals** at `/home/moltbot/.npm-global/lib/node_modules/clawdbot/skills/`
**⚠️ NEVER copy these into agent workspaces without understanding them**

These skills control core bot functionality. Modifying them can break bots.

## How to Use
- Read these to understand what Clawdbot can do natively
- When building new skills, check here first — don't reinvent what already exists
- If you need to extend a core skill, create a wrapper in cold-lava-custom/, not here

## Available Core Skills (52)

| Skill | Description |
|-------|-------------|
| 1password | Set up and use 1Password CLI (op) for secrets management |
| apple-notes | Manage Apple Notes via the `memo` CLI on macOS |
| apple-reminders | Manage Apple Reminders via the `remindctl` CLI on macOS |
| bear-notes | Create, search, and manage Bear notes via grizzly CLI |
| bird | X/Twitter CLI for reading, searching, posting, and engagement |
| blogwatcher | Monitor blogs and RSS/Atom feeds for updates |
| blucli | BluOS CLI for discovery, playback, grouping, and volume |
| bluebubbles | Build or update the BlueBubbles external channel plugin |
| camsnap | Capture frames or clips from RTSP/ONVIF cameras |
| canvas | Display HTML content on connected Clawdbot nodes |
| clawdhub | Search, install, update, and publish agent skills from clawdhub.com |
| coding-agent | Run Codex CLI, Claude Code, OpenCode, or Pi Coding Agent |
| discord | Control Discord from Clawdbot (messages, reactions, stickers, polls, threads, moderation) |
| eightctl | Control Eight Sleep pods (status, temperature, alarms, schedules) |
| food-order | Reorder Foodora orders + track ETA/status |
| gemini | Gemini CLI for one-shot Q&A, summaries, and generation |
| gifgrep | Search GIF providers, download results, extract stills/sheets |
| github | Interact with GitHub using the `gh` CLI |
| gog | Google Workspace CLI for Gmail, Calendar, Drive, Contacts, Sheets, Docs |
| goplaces | Query Google Places API (New) via the goplaces CLI |
| himalaya | CLI to manage emails via IMAP/SMTP |
| imsg | iMessage/SMS CLI for listing chats, history, watch, and sending |
| local-places | Search for places via Google Places API proxy |
| mcporter | List, configure, auth, and call MCP servers/tools directly |
| model-usage | Summarize per-model usage/cost data from CodexBar |
| nano-banana-pro | Generate or edit images via Gemini 3 Pro Image |
| nano-pdf | Edit PDFs with natural-language instructions |
| notion | Notion API for creating and managing pages, databases, and blocks |
| obsidian | Work with Obsidian vaults and automate via obsidian-cli |
| openai-image-gen | Batch-generate images via OpenAI Images API |
| openai-whisper | Local speech-to-text with Whisper CLI (no API key) |
| openai-whisper-api | Transcribe audio via OpenAI Audio Transcriptions API |
| openhue | Control Philips Hue lights/scenes via OpenHue CLI |
| oracle | Best practices for using the oracle CLI |
| ordercli | Foodora-only CLI for past orders and active order status |
| peekaboo | Capture and automate macOS UI with Peekaboo CLI |
| sag | ElevenLabs text-to-speech with mac-style say UX |
| session-logs | Search and analyze your own session logs |
| sherpa-onnx-tts | Local text-to-speech via sherpa-onnx (offline, no cloud) |
| skill-creator | Create or update AgentSkills with scripts, references, and assets |
| slack | Control Slack from Clawdbot (messages, reactions, pins) |
| songsee | Generate spectrograms and visualizations from audio |
| sonoscli | Control Sonos speakers (discover/status/play/volume/group) |
| spotify-player | Terminal Spotify playback/search via spogo |
| summarize | Summarize or extract text/transcripts from URLs, podcasts, local files |
| things-mac | Manage Things 3 via the `things` CLI on macOS |
| tmux | Remote-control tmux sessions for interactive CLIs |
| trello | Manage Trello boards, lists, and cards via REST API |
| video-frames | Extract frames or short clips from videos using ffmpeg |
| voice-call | Start voice calls via the Clawdbot voice-call plugin |
| wacli | Send WhatsApp messages or search/sync WhatsApp history |
| weather | Get current weather and forecasts (no API key required) |
