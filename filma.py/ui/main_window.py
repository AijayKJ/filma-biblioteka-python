import tkinter as tk
from tkinter import ttk

from ui.forms import build_form
from ui.theme import ACCENT, BG, BORDER, FIELD, GREY, MUTED, PANEL, SIDEBAR, WHITE, setup_style
from ui.content import refresh_content

def build_interface(app):

    setup_style(app)

    app.title("Filmu bibliotēka")
    app.geometry("1500x900")
    app.minsize(1120, 700)

    # -------------------------------------------------
    # SĀNU IZVĒLNE
    # -------------------------------------------------

    app.sidebar = tk.Frame(
        app,
        bg=SIDEBAR,
        width=225
    )

    app.sidebar.pack(
        side="left",
        fill="y"
    )

    app.sidebar.pack_propagate(False)

    tk.Label(
        app.sidebar,
        text="KINOTEKA",
        bg=SIDEBAR,
        fg=WHITE,
        font=("Segoe UI", 18, "bold")
    ).pack(
        anchor="w",
        padx=24,
        pady=(32, 3)
    )

    tk.Label(
        app.sidebar,
        text="FILMU DATUBĀZE",
        bg=SIDEBAR,
        fg=MUTED,
        font=("Segoe UI", 8, "bold")
    ).pack(
        anchor="w",
        padx=25,
        pady=(0, 30)
    )

    tk.Frame(
        app.sidebar,
        bg=BORDER,
        height=1
    ).pack(
        fill="x",
        padx=20,
        pady=(0, 18)
    )

    tk.Label(
        app.sidebar,
        text="DATUBĀZE",
        bg=SIDEBAR,
        fg=MUTED,
        font=("Segoe UI", 8, "bold")
    ).pack(
        anchor="w",
        padx=24,
        pady=(0, 10)
    )

    app.nav_buttons = {}

    navigation = [
        ("movies", "Filmas"),
        ("actors", "Aktieri"),
        ("directors", "Režisori"),
        ("genres", "Žanri"),
        ("studios", "Studijas"),
        ("users", "Lietotāji"),
        ("watchlist_items", "Skatīšanās saraksti"),
        ("reviews", "Atsauksmes"),
        ("movie_cast", "Filmu lomas"),
        ("movie_awards", "Filmu balvas")
    ]

    for table, title in navigation:

        button = tk.Button(
            app.sidebar,
            text=title,
            command=lambda t=table: app.change_table(t),
            bg=SIDEBAR,
            fg=GREY,
            activebackground="#303741",
            activeforeground=ACCENT,
            relief="flat",
            bd=0,
            anchor="w",
            padx=24,
            pady=10,
            cursor="hand2",
            font=("Segoe UI", 9)
        )

        button.pack(
            fill="x",
            padx=9,
            pady=1
        )

        app.nav_buttons[table] = button

    tk.Frame(
        app.sidebar,
        bg=BORDER,
        height=1
    ).pack(
        fill="x",
        padx=20,
        pady=20
    )

    tk.Label(
        app.sidebar,
        text="SQLite datubāze  •  lokāla",
        bg=SIDEBAR,
        fg=MUTED,
        font=("Segoe UI", 8)
    ).pack(
        side="bottom",
        pady=22
    )

    # -------------------------------------------------
    # GALVENAIS SATURS
    # -------------------------------------------------

    app.main_area = tk.Frame(
        app,
        bg=BG
    )

    app.main_area.pack(
        side="left",
        fill="both",
        expand=True
    )

    # AUGŠĒJĀ JOSLA

    header = tk.Frame(
        app.main_area,
        bg=BG
    )

    header.pack(
        fill="x",
        padx=32,
        pady=(28, 18)
    )

    app.page_title = tk.Label(
        header,
        text="Filmas",
        bg=BG,
        fg=WHITE,
        font=("Segoe UI", 25, "bold")
    )

    app.page_title.pack(
        side="left"
    )

    # MEKLĒŠANA

    app.search_var = tk.StringVar()

    search_wrap = tk.Frame(
        header,
        bg=FIELD,
        highlightthickness=1,
        highlightbackground=BORDER
    )

    search_wrap.pack(
        side="right"
    )

    tk.Label(
        search_wrap,
        text="⌕",
        bg=FIELD,
        fg=ACCENT,
        font=("Segoe UI", 17)
    ).pack(
        side="left",
        padx=(10, 4)
    )

    search = tk.Entry(
        search_wrap,
        textvariable=app.search_var,
        bg=FIELD,
        fg=WHITE,
        insertbackground=ACCENT,
        relief="flat",
        bd=0,
        font=("Segoe UI", 9),
        width=27
    )

    search.pack(
        side="left",
        padx=(2, 12),
        ipady=10
    )

    app.search_var.trace_add(
        "write",
        lambda *args: refresh_content(app)
    )

    # APRAKSTS

    intro = tk.Frame(
        app.main_area,
        bg=BG
    )

    intro.pack(
        fill="x",
        padx=32,
        pady=(0, 18)
    )

    tk.Label(
        intro,
        text="PĀRVALDI SAVU FILMU KOLEKCIJU",
        bg=BG,
        fg=ACCENT,
        font=("Segoe UI", 8, "bold")
    ).pack(anchor="w")

    tk.Label(
        intro,
        text="Viss vienuviet, pārskatāmi.",
        bg=BG,
        fg=GREY,
        font=("Segoe UI", 10)
    ).pack(
        anchor="w",
        pady=(5, 0)
    )

    tk.Frame(
        app.main_area,
        bg=BORDER,
        height=1
    ).pack(
        fill="x",
        padx=32,
        pady=(0, 18)
    )

    # -------------------------------------------------
    # DARBA LAUKUMS
    # -------------------------------------------------

    body = tk.Frame(
        app.main_area,
        bg=BG
    )

    body.pack(
        fill="both",
        expand=True,
        padx=32,
        pady=(0, 25)
    )

    app.content = tk.Frame(
        body,
        bg=BG
    )

    app.content.pack(
        side="left",
        fill="both",
        expand=True
    )

    app.form_panel = tk.Frame(
        body,
        bg=PANEL,
        width=310,
        padx=18,
        pady=18
    )

    app.form_panel.pack(
        side="right",
        fill="y",
        padx=(22, 0)
    )

    app.form_panel.pack_propagate(False)

    build_form(app)

    refresh_content(app)


# =====================================================
# SATURA ATJAUNOŠANA
# =====================================================

