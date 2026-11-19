import tkinter as tk
from tkinter import ttk


import tkinter as tk
from tkinter import ttk


# =====================================================
# KRĀSU PALETE
# =====================================================

BG = "#101318"
SIDEBAR = "#171B22"
PANEL = "#1A2029"
FIELD = "#222A35"

WHITE = "#EDF1F5"
GREY = "#A2ACB8"
MUTED = "#737F8D"

ACCENT = "#D5A45B"
BORDER = "#2B3542"
DANGER = "#A84F55"


# =====================================================
# TABULU NOSAUKUMI
# =====================================================

TABLE_TITLES = {
    "movies": "Filmas",
    "actors": "Aktieri",
    "directors": "Režisori",
    "genres": "Žanri",
    "studios": "Studijas",
    "users": "Lietotāji",
    "watchlist_items": "Skatīšanās saraksti",
    "reviews": "Atsauksmes",
    "movie_cast": "Filmu lomas",
    "movie_awards": "Filmu balvas"
}


# =====================================================
# STILS
# =====================================================

def setup_style(app):

    app.configure(bg=BG)

    style = ttk.Style()
    style.theme_use("clam")

    style.configure(
        "Treeview",
        background=PANEL,
        foreground=WHITE,
        fieldbackground=PANEL,
        rowheight=38,
        font=("Segoe UI", 9),
        borderwidth=0
    )

    style.configure(
        "Treeview.Heading",
        background=FIELD,
        foreground=GREY,
        font=("Segoe UI", 8, "bold"),
        padding=12,
        relief="flat"
    )

    style.map(
        "Treeview",
        background=[("selected", "#39414B")],
        foreground=[("selected", WHITE)]
    )

    style.configure(
        "TCombobox",
        fieldbackground=FIELD,
        background=FIELD,
        foreground=WHITE,
        arrowcolor=ACCENT,
        bordercolor=BORDER,
        lightcolor=BORDER,
        darkcolor=BORDER,
        padding=8
    )

    style.map(
        "TCombobox",
        fieldbackground=[("readonly", FIELD)],
        foreground=[("readonly", WHITE)]
    )

    style.configure(
        "Vertical.TScrollbar",
        background=FIELD,
        troughcolor=BG,
        bordercolor=BG,
        arrowcolor=GREY
    )


# =====================================================
# POGAS
# =====================================================

def make_button(parent, text, command, color=FIELD, fg=WHITE):

    return tk.Button(
        parent,
        text=text,
        command=command,
        bg=color,
        fg=fg,
        activebackground=ACCENT,
        activeforeground="#17191D",
        relief="flat",
        bd=0,
        padx=14,
        pady=11,
        cursor="hand2",
        font=("Segoe UI", 9, "bold")
    )


# =====================================================
# IEVADES LAUKI
# =====================================================

