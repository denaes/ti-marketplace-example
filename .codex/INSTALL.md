# Installing Orbit for Codex

Enable Orbit skills in Codex via native skill discovery.

## Installation

1. **Clone the Orbit repository:**
   ```bash
   git clone https://github.com/denaes/ti-marketplace-example.git ~/.codex/orbit
   ```

2. **Create the skills symlink:**
   ```bash
   mkdir -p ~/.agents/skills
   ln -s ~/.codex/orbit/skills ~/.agents/skills/orbit
   ```

   **Windows (PowerShell):**
   ```powershell
   New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.agents\skills"
   cmd /c mklink /J "$env:USERPROFILE\.agents\skills\orbit" "$env:USERPROFILE\.codex\orbit\skills"
   ```

3. **Restart Codex** to discover the skills.

## Updating

```bash
cd ~/.codex/orbit && git pull
```

## Uninstalling

```bash
rm ~/.agents/skills/orbit
rm -rf ~/.codex/orbit
```
