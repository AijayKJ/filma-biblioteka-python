import tkinter as tk
from tkinter import ttk

from ui.theme import ACCENT, BG, BORDER, GREY, MUTED, PANEL, SIDEBAR, TABLE_TITLES, WHITE

def refresh_content(app):

    if not hasattr(app, "content"):
        return

    for widget in app.content.winfo_children():
        widget.destroy()

    table = app.current_table

    search = app.search_var.get().strip().lower()

    app.page_title.configure(
        text=TABLE_TITLES[table]
    )

    # AKTĪVĀ IZVĒLNE

    for name, button in app.nav_buttons.items():

        active = name == table

        button.configure(
            bg="#303741" if active else SIDEBAR,
            fg=ACCENT if active else GREY,
            font=(
                "Segoe UI",
                9,
                "bold" if active else "normal"
            )
        )

    records = app.get_records(table)

    # MEKLĒŠANA

    if search:

        filtered = []

        for record in records:

            values = [
                str(value)
                for value in record
                if value is not None
            ]

            for field, value in zip(
                app.TABULAS[table],
                record[1:]
            ):

                values.append(
                    app.display_value(field, value)
                )

            text = " ".join(values).lower()

            if search in text:
                filtered.append(record)

        records = filtered

    tk.Label(
        app.content,
        text=f"{len(records)} IERAKSTI",
        bg=BG,
        fg=MUTED,
        font=("Segoe UI", 8, "bold")
    ).pack(
        anchor="w",
        pady=(0, 10)
    )

    show_table(app, records)


# =====================================================
# DATU TABULA
# =====================================================

def show_table(app, records):

    table = app.current_table

    columns = ["id"] + app.TABULAS[table]

    wrap = tk.Frame(
        app.content,
        bg=PANEL,
        highlightthickness=1,
        highlightbackground=BORDER
    )

    wrap.pack(
        fill="both",
        expand=True
    )

    tree = ttk.Treeview(
        wrap,
        columns=columns,
        show="headings",
        selectmode="browse"
    )

    ybar = ttk.Scrollbar(
        wrap,
        orient="vertical",
        command=tree.yview
    )

    xbar = ttk.Scrollbar(
        wrap,
        orient="horizontal",
        command=tree.xview
    )

    tree.configure(
        yscrollcommand=ybar.set,
        xscrollcommand=xbar.set
    )

    # KOLONNAS

    for column in columns:

        if column == "id":
            heading = "ID"
            width = 65

        else:
            heading = app.LAUKE_NOSAUKUMI.get(
                column,
                column.replace("_", " ").upper()
            ).upper()

            width = 190 if column in (
                "title", "synopsis", "body", "description"
            ) else 135

        tree.heading(
            column,
            text=heading
        )

        tree.column(
            column,
            width=width,
            minwidth=80,
            anchor="w",
            stretch=True
        )

    # IERAKSTI

    for record in records:

        shown = [record[0]]

        for field, value in zip(
            app.TABULAS[table],
            record[1:]
        ):

            shown.append(
                app.display_value(field, value)
            )

        tree.insert(
            "",
            "end",
            iid=str(record[0]),
            values=shown
        )

    tree.grid(
        row=0,
        column=0,
        sticky="nsew"
    )

    ybar.grid(
        row=0,
        column=1,
        sticky="ns"
    )

    xbar.grid(
        row=1,
        column=0,
        sticky="ew"
    )

    wrap.grid_rowconfigure(
        0,
        weight=1
    )

    wrap.grid_columnconfigure(
        0,
        weight=1
    )

    tree.bind(
        "<<TreeviewSelect>>",
        lambda event: select_tree_record(app, tree)
    )

    app.current_tree = tree

    if not records:

        tk.Label(
            app.content,
            text="Šeit pagaidām nav ierakstu.",
            bg=BG,
            fg=GREY,
            font=("Segoe UI", 11)
        ).pack(
            anchor="w",
            pady=18
        )


# =====================================================
# IERAKSTA IZVĒLE
# =====================================================

def select_tree_record(app, tree):

    selected = tree.selection()

    if selected:

        record_id = int(selected[0])

        record = app.get_record(
            app.current_table,
            record_id
        )

        if record:
            app.select_record(record)
