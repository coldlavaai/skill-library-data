# Cold Lava Skill Library Data

Auto-synced from the Cold Lava fleet server.

This repository contains all packaged skills for the agent fleet. Used by:
- **Skill Library Dashboard** (https://skill-library-dashboard.vercel.app)
- Individual agents pulling skills for deployment

## Structure

\`\`\`
skill-name/
├── SKILL.md          # Main instructions
├── scripts/          # Automation scripts
├── references/       # Reference docs
├── templates/        # Output templates
└── README.md         # Description
\`\`\`

## Sync

Auto-synced every time a skill is added or modified. Do not edit this repo directly — changes will be overwritten.

Edit skills in \`/home/moltbot/skill-library/\` on the fleet server.

**Last sync:** $(date -u +"%Y-%m-%d %H:%M UTC")
