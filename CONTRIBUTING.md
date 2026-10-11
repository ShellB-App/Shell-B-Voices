# Contributing a voice

1. Fork the repository and add a folder `voices/<id>/` with a `voice.json`. The id is lowercase letters, digits and
   dashes (`harbor`, `little-robot`), and it must not already exist.
2. Fill in `name`, `label`, `description`, `author` and `license` (an SPDX id: CC0-1.0, MIT, CC-BY-4.0). By opening a
   pull request you agree that the description is shared under the license you named.
3. Run `python3 -I scripts/validate.py` from the repository root and fix every error.
4. Design the voice in your own Shell:B from exactly the text in the file and listen to a few sentences of different
   kinds: a question, a list, a long paragraph. If you had to tweak the description to get there, put the tweak in the
   file.
5. Commit the folder (and `sample.mp3` if you made one) with the updated `index.json`, and open a pull request that
   says what the voice is for.

Voices are reviewed for the description and for the result: a clear character, a voice that is pleasant to hear for
an hour, a label that says what it is. Descriptions that imitate a real person, a named character, or a voice from a
film or game are not merged, however the description is phrased.

Updating a voice: bump `version`, keep the id.
