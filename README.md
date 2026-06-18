# 🎵 Playlist Manager

A music playlist manager built for the Ansr take-home assignment — create playlists, add/remove songs, rename and delete playlists, and browse everything through a Netflix-inspired dark UI.

## Live Demo
[Hugging Face Spaces](https://huggingface.co/spaces/adishateja/playlist-manager)

## Features
- Create a playlist (blocks empty/duplicate names)
- Rename a playlist (blocks empty names and name collisions)
- Delete a playlist
- Add a song to a playlist (blocks empty fields and exact duplicates)
- Remove a song from a playlist
- View all playlists with song counts, and inspect any single playlist's full song list

## Tech Stack
- **Python** — core logic
- **Gradio** — web UI
- **In-memory storage** — a Python dict, no database (see Assumptions)
- **pytest** — unit tests for validation/edge cases

## Setup & Run
```bash
git clone <your-repo-url>
cd playlist-manager
pip install -r requirements.txt
python app.py
```
Open the local URL Gradio prints (usually `http://127.0.0.1:7860`).

To run tests:
```bash
pytest test_playlist_manager.py -v
```

## Assumptions
- **No persistence**: data is stored in memory and resets whenever the app restarts (including on Hugging Face Spaces, which can sleep after inactivity). This was a deliberate scope choice for a demo, not an oversight.
- **Single user, no auth**: the assignment didn't call for multi-user support, so there's no login/accounts.
- **Case-insensitive matching**: playlist names and song title+artist pairs are matched case-insensitively for duplicate detection, but displayed with whatever casing the user typed.
- **Song identity**: a song is uniquely identified by (title, artist) together — two different artists can both have a song called "Imagine" without conflict.

## AI Tools Used
This project was built with Claude (Anthropic), used as a pair-programming partner end-to-end: deciding the stack (storage layer, UI framework, deployment target) explicitly through pros/cons discussion rather than letting the AI choose unprompted, designing the data model and validation rules before any code was written, then generating the core logic, Gradio UI, and pytest suite. Claude was also used to debug a Colab `%%writefile` issue (a missing magic-command line caused silent file-write failures) and to iterate on the UI theme through Gradio's theme-builder API rather than fragile custom CSS.

The main challenge was Hugging Face Spaces build failures that surfaced as unhelpful cache-log output rather than the actual Python error — solved by checking the dedicated build/container logs for the real traceback instead of the top-level summary, and by re-pasting clean file contents to rule out copy-paste corruption.
