## Contributing

Thank you for improving this project! Please follow these guidelines to keep changes easy to review and safe to ship.

### Local development
```bash
cd "/path/to/yesand-music"
python3 -m venv .venv
source .venv/bin/activate
pip3 install --upgrade pip setuptools wheel
pip3 install mido python-rtmidi
python3 main.py
```

### Code style
- Prefer clear, descriptive names over abbreviations.
- Keep functions small and focused; avoid deep nesting.
- Add concise docstrings explaining purpose and behavior.

### Branching & PRs
- Create feature branches from `main` (e.g., `feat/arpeggiator`, `fix/port-detection`).
- Keep PRs small and focused with a clear description and testing steps.
- Note any platform-specific testing (macOS, Apple Silicon, DAW versions).

### Commit messages
- Use imperative style: "Add X", "Fix Y".
- Reference issues when applicable: `Fixes #123`.

### Testing changes
- Manual test: run `python3 main.py` and verify the C Major scale plays.
- If changing scheduling or output, add a brief note in the PR describing expected audible behavior.

### Roadmap (control plane)
- M1: Core control plane
  - Intent parser (regex/keywords), session state, MIDI dispatcher using `MidiPlayer`.
  - Commands: play scale/arp/random, set key/scale, density/register/velocity/randomness, cc, stop.
- M2: Manifest support
  - Load `project.yaml`/`project.json` with parts and CC aliases; map logical parts to targets.
- M3: Optional UI read
  - macOS Accessibility-based read of track names and armed/selected state; feature-flag and degrade on failure.
- M4: Audio hints (optional)
  - Loopback capture and lightweight key estimation command (advisory only).

See `docs/CONTROL_PLANE.md` for design details.


