"""
Core logic for the playlist manager.
Pure functions, no UI dependencies — every function returns a plain string
status message or data structure, so this module can be tested and reused
independently of Gradio.
"""

from typing import Optional, Union

playlists: dict[str, list[dict[str, str]]] = {}


def _find_playlist_key(name: str) -> Optional[str]:
    """Case-insensitive lookup of the real stored playlist key."""
    target = name.strip().lower()
    for existing in playlists:
        if existing.lower() == target:
            return existing
    return None


def _find_song_index(playlist_key: str, title: str, artist: str) -> Optional[int]:
    """Case-insensitive lookup of a song's index within a playlist."""
    title = title.strip().lower()
    artist = artist.strip().lower()
    for i, song in enumerate(playlists[playlist_key]):
        if song["title"].strip().lower() == title and song["artist"].strip().lower() == artist:
            return i
    return None


def create_playlist(name: str) -> str:
    name = name.strip()
    if not name:
        return "Error: Playlist name cannot be empty."
    if _find_playlist_key(name) is not None:
        return f"Error: A playlist named '{name}' already exists."
    playlists[name] = []
    return f"Playlist '{name}' created."


def delete_playlist(name: str) -> str:
    match = _find_playlist_key(name)
    if match is None:
        return f"Error: Playlist '{name.strip()}' not found."
    del playlists[match]
    return f"Playlist '{match}' deleted."


def rename_playlist(old_name: str, new_name: str) -> str:
    new_name = new_name.strip()
    old_match = _find_playlist_key(old_name)
    if old_match is None:
        return f"Error: Playlist '{old_name.strip()}' not found."
    if not new_name:
        return "Error: New playlist name cannot be empty."
    new_match = _find_playlist_key(new_name)
    if new_match is not None and new_match != old_match:
        return f"Error: A playlist named '{new_name}' already exists."
    songs = playlists.pop(old_match)
    playlists[new_name] = songs
    return f"Playlist '{old_match}' renamed to '{new_name}'."


def add_song(playlist_name: str, title: str, artist: str) -> str:
    match = _find_playlist_key(playlist_name)
    if match is None:
        return f"Error: Playlist '{playlist_name.strip()}' not found."

    title = title.strip()
    artist = artist.strip()
    if not title or not artist:
        return "Error: Both song title and artist are required."

    if _find_song_index(match, title, artist) is not None:
        return f"Error: '{title}' by {artist} is already in '{match}'."

    playlists[match].append({"title": title, "artist": artist})
    return f"Added '{title}' by {artist} to '{match}'."


def remove_song(playlist_name: str, title: str, artist: str) -> str:
    match = _find_playlist_key(playlist_name)
    if match is None:
        return f"Error: Playlist '{playlist_name.strip()}' not found."

    idx = _find_song_index(match, title, artist)
    if idx is None:
        return f"Error: '{title.strip()}' by {artist.strip()} not found in '{match}'."

    playlists[match].pop(idx)
    return f"Removed '{title.strip()}' by {artist.strip()} from '{match}'."


def list_playlists() -> list[tuple[str, int]]:
    """Returns [(playlist_name, song_count), ...] sorted alphabetically."""
    return sorted(
        [(name, len(songs)) for name, songs in playlists.items()],
        key=lambda x: x[0].lower()
    )


def get_playlist(name: str):
    """Returns the list of song dicts for a playlist, or an error string."""
    match = _find_playlist_key(name)
    if match is None:
        return f"Error: Playlist '{name.strip()}' not found."
    return playlists[match]