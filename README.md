# Shell:B Voices

[![Validate](https://github.com/ShellB-App/Shell-B-Voices/actions/workflows/validate.yml/badge.svg)](https://github.com/ShellB-App/Shell-B-Voices/actions/workflows/validate.yml) [![MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Community voices for [Shell:B](https://github.com/ShellB-App/Shell-B), the local-first AI workspace.
Part of the family with [Shell-B-Themes](https://github.com/ShellB-App/Shell-B-Themes), [Shell-B-Screensavers](https://github.com/ShellB-App/Shell-B-Screensavers) and [Shell-B-Agents](https://github.com/ShellB-App/Shell-B-Agents).

A Shell:B voice is **a description, not a recording**. HERMES, Shell:B's speech service, designs voices from text with
Qwen3-TTS: you describe a speaker (age, accent, pitch, pace, mood), it makes a reference clip, and from then on that
voice reads anything in that character. A voice file here holds the description, an optional tone instruction and the
line the reference clip reads. No audio is stored; the voice is designed on the machine that installs it, so the
repository stays tiny and nobody's actual voice is in it.

## Install one

Open **Settings → Speech**, find the voice library, and press **Describe**. Paste the `description` from the voice's
`voice.json`, use its `refText` as the reference line if it has one, listen to the draft, and keep it. The `style`
line goes in the voice's tone instruction. The voice then appears under *Your voices* in every voice picker, and any
agent can be given it.

One-click install from Settings, the way themes and screensavers work, is planned.

## Catalogue

| Voice | Sounds like | For |
|---|---|---|
| Harbor | A low, calm man in his fifties, a little gravel | Narration, long reads, late nights |
| Lark | A bright young British woman, quick and friendly | A day-to-day assistant |
| Quill | A crisp, neutral newsreader | Morning briefs, documents, numbers |
| Marrow | An old, gravelly storyteller with long pauses | Bedtime stories, legends, game masters |
| Juniper | A warm, wry Scottish woman | Conversation, recipes, letters |
| Pixel | A small, cheerful robot | Timers, reminders, games with children |

`index.json` is the machine-readable version of this table.

## Make one

Design it in Shell:B first (Settings → Speech, voice library, Describe), iterate on the description until the draft sounds
right, then copy the description into a `voice.json`. Every voice is a folder under `voices/`:

```jsonc
{
  "name": "Harbor",                          // 1-32 characters
  "label": "Harbor · low, calm male",        // ≤ 60 characters, what the picker shows
  "description": "A man in his fifties with a low, even voice …",   // 40-600 characters: the voice design
  "style": "Calm and unhurried. Pause at commas.",                 // optional tone instruction, ≤ 200
  "language": "en",                          // en, fr, en-GB …
  "refText": "The line the reference clip reads.",                 // optional, ≤ 300 characters
  "tags": ["male", "calm"],
  "author": "Your name",
  "license": "CC0-1.0",                      // an SPDX id
  "version": "1.0"
}
```

An optional `sample.mp3` (≤ 400 KB) made on your own machine lets people hear it before designing it.

What makes a description work: concrete physical facts (age range, pitch, pace, accent, breathiness, where the voice
sits in the chest or the head), one or two personality words, and the situation it suits. What doesn't: a real
person's name. The validator refuses descriptions that read as an impression of someone; describe a voice, not a
person.

Then check it:

```bash
python3 -I scripts/validate.py
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for the pull request checklist.

## Other collections

Shell:B installs from the whole family: [Shell-B-Themes](https://github.com/ShellB-App/Shell-B-Themes), [Shell-B-Screensavers](https://github.com/ShellB-App/Shell-B-Screensavers) and [Shell-B-Agents](https://github.com/ShellB-App/Shell-B-Agents) work the same way, with a validator, CI and a one-screen checklist each. Found a bug in the app itself? That goes to [Shell-B issues](https://github.com/ShellB-App/Shell-B/issues); questions and show-and-tell to [Discussions](https://github.com/ShellB-App/Shell-B/discussions).

## License

The scripts and this repository are MIT. Each voice names its own license in `voice.json`; the ones here are CC0.
