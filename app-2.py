
import gradio as gr
from playlist_manager import (
    create_playlist, delete_playlist, rename_playlist,
    add_song, remove_song, list_playlists, get_playlist, playlists
)

# ---------- Theme ----------
# Built via gr.themes...set() (theme builder), not raw CSS targeting Gradio's
# internal classes — survives version bumps.
netflix_theme = gr.themes.Base(
    primary_hue="red",
    secondary_hue="gray",
    neutral_hue="gray",
    font=gr.themes.GoogleFont("Inter"),
).set(
    body_background_fill="#141414",
    body_background_fill_dark="#141414",
    body_text_color="#e5e5e5",
    body_text_color_dark="#e5e5e5",
    body_text_color_subdued="#808080",
    block_background_fill="#1f1f1f",
    block_background_fill_dark="#1f1f1f",
    block_border_color="#2a2a2a",
    block_border_color_dark="#2a2a2a",
    block_title_text_color="#ffffff",
    block_title_text_color_dark="#ffffff",
    block_label_text_color="#b3b3b3",
    block_label_text_color_dark="#b3b3b3",
    input_background_fill="#0e0e0e",
    input_background_fill_dark="#0e0e0e",
    input_border_color="#3a3a3a",
    input_border_color_dark="#3a3a3a",
    input_border_color_focus="#e50914",
    input_border_color_focus_dark="#e50914",
    button_primary_background_fill="#e50914",
    button_primary_background_fill_hover="#f6121d",
    button_primary_text_color="#ffffff",
    button_secondary_background_fill="#2a2a2a",
    button_secondary_background_fill_hover="#3a3a3a",
    button_secondary_text_color="#e5e5e5",
    button_cancel_background_fill="#3a0d10",
    button_cancel_background_fill_hover="#5c1318",
    button_cancel_text_color="#ff6b6b",
    border_color_primary="#2a2a2a",
    shadow_drop="0 4px 14px rgba(0, 0, 0, 0.5)",
)

custom_css = """
.gradio-container {
    background: #141414 !important;
}

.netflix-title h1 {
    font-weight: 800 !important;
    letter-spacing: 1px;
    color: #e50914 !important;
    text-transform: uppercase;
    font-size: 2.2em !important;
}

.netflix-subtitle p {
    color: #808080 !important;
}
"""


def playlist_choices():
    return sorted(playlists.keys(), key=str.lower)


def refresh_overview():
    data = list_playlists()
    if not data:
        return [["No playlists yet", ""]]
    return [[name, count] for name, count in data]


def refresh_song_choices(playlist_name):
    result = get_playlist(playlist_name) if playlist_name else []
    if isinstance(result, str) or not result:
        return gr.update(choices=[], value=None)
    labels = [f'{s["title"]} — {s["artist"]}' for s in result]
    return gr.update(choices=labels, value=None)


def view_playlist(playlist_name):
    if not playlist_name:
        return [["Select a playlist above", ""]]
    result = get_playlist(playlist_name)
    if isinstance(result, str):
        return [[result, ""]]
    if not result:
        return [["No songs yet — add your first one", ""]]
    return [[s["title"], s["artist"]] for s in result]


def _refresh_all_playlist_dropdowns():
    choices = playlist_choices()
    return tuple(gr.update(choices=choices) for _ in range(5))


def do_create(name):
    msg = create_playlist(name)
    return msg, *_refresh_all_playlist_dropdowns(), refresh_overview()


def do_delete(name):
    msg = delete_playlist(name)
    return msg, *_refresh_all_playlist_dropdowns(), refresh_overview()


def do_rename(old_name, new_name):
    msg = rename_playlist(old_name, new_name)
    return msg, *_refresh_all_playlist_dropdowns(), refresh_overview()


def do_add_song(playlist_name, title, artist):
    msg = add_song(playlist_name, title, artist)
    return msg, refresh_song_choices(playlist_name), refresh_overview()


def do_remove_song(playlist_name, song_label):
    if not song_label:
        return "Select a song to remove.", refresh_song_choices(playlist_name), refresh_overview()
    title, artist = [s.strip() for s in song_label.split("—", 1)]
    msg = remove_song(playlist_name, title, artist)
    return msg, refresh_song_choices(playlist_name), refresh_overview()


with gr.Blocks(title="Playlist Manager", theme=netflix_theme, css=custom_css) as demo:
    gr.Markdown("# 🎵 PLAYLIST MANAGER", elem_classes="netflix-title")
    gr.Markdown("Create, organize, and manage your playlists", elem_classes="netflix-subtitle")

    with gr.Tab("Playlists"):
        gr.Markdown("### Create")
        new_name = gr.Textbox(label="Playlist name", placeholder="Road Trip")
        create_btn = gr.Button("Create Playlist", variant="primary")
        create_status = gr.Textbox(label="Status", interactive=False)

        gr.Markdown("### Rename")
        rename_old = gr.Dropdown(choices=playlist_choices(), label="Existing playlist")
        rename_new = gr.Textbox(label="New name")
        rename_btn = gr.Button("Rename Playlist", variant="primary")
        rename_status = gr.Textbox(label="Status", interactive=False)

        gr.Markdown("### Delete")
        delete_select = gr.Dropdown(choices=playlist_choices(), label="Playlist to delete")
        delete_btn = gr.Button("Delete Playlist", variant="stop")
        delete_status = gr.Textbox(label="Status", interactive=False)

    with gr.Tab("Songs"):
        gr.Markdown("### Add a song")
        add_playlist_select = gr.Dropdown(choices=playlist_choices(), label="Playlist")
        song_title = gr.Textbox(label="Song title", placeholder="Imagine")
        song_artist = gr.Textbox(label="Artist", placeholder="John Lennon")
        add_song_btn = gr.Button("Add Song", variant="primary")
        add_song_status = gr.Textbox(label="Status", interactive=False)

        gr.Markdown("### Remove a song")
        remove_playlist_select = gr.Dropdown(choices=playlist_choices(), label="Playlist")
        remove_song_select = gr.Dropdown(choices=[], label="Song to remove")
        remove_song_btn = gr.Button("Remove Song", variant="stop")
        remove_song_status = gr.Textbox(label="Status", interactive=False)

    with gr.Tab("View"):
        gr.Markdown("### All playlists")
        overview_table = gr.Dataframe(headers=["Playlist", "Song Count"], value=refresh_overview())
        refresh_btn = gr.Button("Refresh", variant="secondary")

        gr.Markdown("### Inspect one playlist")
        view_select = gr.Dropdown(choices=playlist_choices(), label="Playlist")
        view_table = gr.Dataframe(headers=["Title", "Artist"])

    create_btn.click(
        do_create, inputs=[new_name],
        outputs=[create_status, rename_old, delete_select, add_playlist_select,
                 remove_playlist_select, view_select, overview_table]
    )

    rename_btn.click(
        do_rename, inputs=[rename_old, rename_new],
        outputs=[rename_status, rename_old, delete_select, add_playlist_select,
                 remove_playlist_select, view_select, overview_table]
    )

    delete_btn.click(
        do_delete, inputs=[delete_select],
        outputs=[delete_status, rename_old, delete_select, add_playlist_select,
                 remove_playlist_select, view_select, overview_table]
    )

    add_song_btn.click(
        do_add_song, inputs=[add_playlist_select, song_title, song_artist],
        outputs=[add_song_status, remove_song_select, overview_table]
    )

    remove_song_btn.click(
        do_remove_song, inputs=[remove_playlist_select, remove_song_select],
        outputs=[remove_song_status, remove_song_select, overview_table]
    )

    remove_playlist_select.change(
        refresh_song_choices, inputs=[remove_playlist_select], outputs=[remove_song_select]
    )

    refresh_btn.click(refresh_overview, outputs=[overview_table])

    view_select.change(view_playlist, inputs=[view_select], outputs=[view_table])


if __name__ == "__main__":
    demo.launch()