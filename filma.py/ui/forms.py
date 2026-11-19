import tkinter as tk
from tkinter import ttk

from app.database import savienot
from ui.theme import ACCENT, BORDER, FIELD, GREY, PANEL, WHITE, make_button

def create_fields(app):

    for widget in app.form_fields.winfo_children():
        widget.destroy()

    app.entries = {}

    table = app.current_table

    for column in app.TABULAS[table]:

        label = app.LAUKE_NOSAUKUMI.get(
            column,
            column.replace("_", " ").title()
        )

        tk.Label(
            app.form_fields,
            text=label.upper(),
            bg=PANEL,
            fg=GREY,
            font=("Segoe UI", 8, "bold")
        ).pack(
            anchor="w",
            pady=(12, 5)
        )

        # ĀRĒJO ATSLĒGU IZVĒLE

        if column in app.FK:

            related_table, label_column = app.FK[column]

            conn = savienot()

            try:

                records = conn.execute(
                    f"SELECT id, {label_column} "
                    f"FROM {related_table} "
                    f"ORDER BY {label_column}"
                ).fetchall()

            finally:
                conn.close()

            options = [
                f"{row[0]} — {row[1]}"
                for row in records
            ]

            entry = ttk.Combobox(
                app.form_fields,
                values=options,
                state="readonly",
                font=("Segoe UI", 9)
            )

            entry.pack(
                fill="x",
                ipady=3
            )

        else:

            entry = tk.Entry(
                app.form_fields,
                bg=FIELD,
                fg=WHITE,
                insertbackground=ACCENT,
                relief="flat",
                bd=0,
                font=("Segoe UI", 9),
                highlightthickness=1,
                highlightbackground=BORDER,
                highlightcolor=ACCENT
            )

            entry.pack(
                fill="x",
                ipady=9
            )

        app.entries[column] = entry


# =====================================================
# IERAKSTU PĀRVALDĪBAS FORMA
# =====================================================
def build_form(app):
    panel = app.form_panel

    tk.Label(
        panel,
        text="IERAKSTA PĀRVALDĪBA",
        bg=PANEL,
        fg=ACCENT,
        font=("Segoe UI", 8, "bold")
    ).pack(
        anchor="w",
        pady=(0, 8)
    )

    tk.Label(
        panel,
        text="Informācija",
        bg=PANEL,
        fg=WHITE,
        font=("Segoe UI", 19, "bold")
    ).pack(anchor="w")

    tk.Label(
        panel,
        text="Pievieno jaunu ierakstu vai rediģē esošu.",
        bg=PANEL,
        fg=GREY,
        font=("Segoe UI", 9),
        wraplength=260,
        justify="left"
    ).pack(
        anchor="w",
        pady=(5, 16)
    )

    # RITINĀMIE IEVADES LAUKI

    form_container = tk.Frame(
        panel,
        bg=PANEL
    )

    form_container.pack(
        fill="both",
        expand=True
    )

    canvas = tk.Canvas(
        form_container,
        bg=PANEL,
        highlightthickness=0
    )
    # Peles ritenīša ritināšana

    def scroll_form(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def linux_scroll_up(event):
        canvas.yview_scroll(-1, "units")

    def linux_scroll_down(event):
        canvas.yview_scroll(1, "units")

    def enable_scroll(event):
        canvas.bind_all("<MouseWheel>", scroll_form)
        canvas.bind_all("<Button-4>", linux_scroll_up)
        canvas.bind_all("<Button-5>", linux_scroll_down)

    def disable_scroll(event):
        canvas.unbind_all("<MouseWheel>")
        canvas.unbind_all("<Button-4>")
        canvas.unbind_all("<Button-5>")

    canvas.bind("<Enter>", enable_scroll)
    canvas.bind("<Leave>", disable_scroll)
    
    scrollbar = ttk.Scrollbar(
        form_container,
        orient="vertical",
        command=canvas.yview
    )

    app.form_fields = tk.Frame(
        canvas,
        bg=PANEL
    )

    app.form_fields.bind(
        "<Configure>",
        lambda event: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas_window = canvas.create_window(
        (0, 0),
        window=app.form_fields,
        anchor="nw"
    )

    canvas.bind(
        "<Configure>",
        lambda event: canvas.itemconfigure(
            canvas_window,
            width=event.width
        )
    )

    canvas.configure(
        yscrollcommand=scrollbar.set
    )

    canvas.pack(
        side="left",
        fill="both",
        expand=True
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    # POGU JOSLA

    app.form_buttons = tk.Frame(
        panel,
        bg=PANEL
    )

    app.form_buttons.pack(
        fill="x",
        side="bottom",
        pady=(15, 0)
    )

    make_button(
        app.form_buttons,
        "Pievienot ierakstu",
        app.add_record,
        ACCENT,
        "#17191D"
    ).pack(
        fill="x",
        pady=3
    )

    make_button(
        app.form_buttons,
        "Saglabāt izmaiņas",
        app.update_record,
        "#35404D"
    ).pack(
        fill="x",
        pady=3
    )

    button_row = tk.Frame(
        app.form_buttons,
        bg=PANEL
    )

    button_row.pack(
        fill="x",
        pady=3
    )

    make_button(
        button_row,
        "Notīrīt",
        app.clear_form
    ).pack(
        side="left",
        fill="x",
        expand=True,
        padx=(0, 4)
    )

    make_button(
        button_row,
        "Dzēst",
        app.delete_record,
        "#482B30"
    ).pack(
        side="left",
        fill="x",
        expand=True,
        padx=(4, 0)
    )

    create_fields(app)


# =====================================================
# GALVENĀ INTERFEISA IZVEIDE
# =====================================================

