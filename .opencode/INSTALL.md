# Installing Orbit for OpenCode

## Installation

Add orbit to the `plugin` array in your `opencode.json`:

```json
{
  "plugin": ["orbit@git+https://github.com/denaes/ti-marketplace-example.git"]
}
```

Restart OpenCode. The plugin auto-installs and registers all skills.

## Updating

Orbit updates automatically when you restart OpenCode.

## Usage

Use OpenCode's native `skill` tool:

```
use skill tool to list skills
use skill tool to load orbit/engineering/test-driven-development
```
