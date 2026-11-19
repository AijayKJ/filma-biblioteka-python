import sqlite3
import tkinter as tk
from tkinter import messagebox

from app.config import FK, LAUKU_NOSAUKUMI, TABULAS
from app.database import savienot
from ui.forms import create_fields
from ui.main_window import build_interface
from ui.content import refresh_content

class FilmuBiblioteka(tk.Tk):

    def __init__(self):
        super().__init__()

        self.TABULAS = TABULAS
        self.FK = FK
        self.LAUKE_NOSAUKUMI = LAUKU_NOSAUKUMI
        self.current_table = "movies"
        self.selected_id = None
        self.current_tree = None
        self.entries = {}

        build_interface(self)

    # TABULU PĀRSLĒGŠANA

    def change_table(self, table):
        self.current_table = table
        self.selected_id = None
        create_fields(self)
        refresh_content(self)

    # DATU NOLASĪŠANA

    def get_records(self, table):
        columns = ["id"] + TABULAS[table]

        conn = savienot()

        try:
            records = conn.execute(
                f"SELECT {', '.join(columns)} FROM {table} ORDER BY id DESC"
            ).fetchall()

            return records

        finally:
            conn.close()

    def get_record(self, table, record_id):
        columns = ["id"] + TABULAS[table]

        conn = savienot()

        try:
            return conn.execute(
                f"SELECT {', '.join(columns)} FROM {table} WHERE id = ?",
                (record_id,)
            ).fetchone()

        finally:
            conn.close()

    # SAISTĪTO TABULU VĒRTĪBAS

    def fk_label(self, field, value):

        if value is None:
            return ""

        table, label_column = FK[field]

        conn = savienot()

        try:
            result = conn.execute(
                f"SELECT {label_column} FROM {table} WHERE id = ?",
                (value,)
            ).fetchone()

            if result:
                return f"{value} — {result[0]}"

            return str(value)

        finally:
            conn.close()

    def display_value(self, field, value):

        if field in FK and value is not None:
            return self.fk_label(field, value)

        if field == "won":
            return "Jā" if value else "Nē"

        return "" if value is None else str(value)

    # IZVĒLĒTĀ IERAKSTA DATI

    def select_record(self, record):

        self.selected_id = record[0]

        for field_name, value in zip(
            self.entries,
            record[1:]
        ):

            widget = self.entries[field_name]

            if field_name in FK:
                widget.set(
                    self.fk_label(field_name, value)
                    if value is not None else ""
                )

            else:
                widget.delete(0, "end")

                if value is not None:
                    widget.insert(0, str(value))

    # FORMAS VĒRTĪBAS

    def get_form_values(self):

        values = []

        for field_name, widget in self.entries.items():

            raw = widget.get().strip()

            if field_name in FK:

                if not raw:
                    values.append(None)
                else:
                    try:
                        values.append(int(raw.split(" — ")[0]))
                    except ValueError:
                        raise ValueError(
                            f"Izvēlies derīgu vērtību laukā "
                            f"{LAUKU_NOSAUKUMI[field_name]}."
                        )

            else:
                values.append(raw or None)

        return values

    # FORMAS NOTĪRĪŠANA

    def clear_form(self):

        for widget in self.entries.values():

            if widget.winfo_class() == "TCombobox":
                widget.set("")
            else:
                widget.delete(0, "end")

        self.selected_id = None

        if self.current_tree is not None:
            self.current_tree.selection_remove(
                self.current_tree.selection()
            )

    # PIEVIENOT IERAKSTU

    def add_record(self):

        try:
            values = self.get_form_values()
        except ValueError as error:
            messagebox.showwarning("Pārbaudi ievadi", str(error))
            return

        if not any(value is not None for value in values):
            messagebox.showwarning(
                "Uzmanību",
                "Vispirms aizpildi ievades laukus."
            )
            return

        columns = ", ".join(TABULAS[self.current_table])

        placeholders = ", ".join(
            ["?"] * len(TABULAS[self.current_table])
        )

        sql = (
            f"INSERT INTO {self.current_table} "
            f"({columns}) VALUES ({placeholders})"
        )

        self.execute_sql(sql, values)

    # LABOT IERAKSTU

    def update_record(self):

        if self.selected_id is None:
            messagebox.showwarning(
                "Uzmanību",
                "Vispirms izvēlies ierakstu."
            )
            return

        try:
            values = self.get_form_values()
        except ValueError as error:
            messagebox.showwarning("Pārbaudi ievadi", str(error))
            return

        changes = ", ".join(
            f"{column} = ?"
            for column in TABULAS[self.current_table]
        )

        sql = (
            f"UPDATE {self.current_table} "
            f"SET {changes}, updated_at = CURRENT_TIMESTAMP "
            f"WHERE id = ?"
        )

        # Tabulās bez updated_at izmanto atsevišķu vaicājumu.
        if self.current_table in (
            "watchlist_items", "movie_cast", "movie_awards"
        ):
            sql = (
                f"UPDATE {self.current_table} "
                f"SET {changes} WHERE id = ?"
            )

        self.execute_sql(
            sql,
            values + [self.selected_id]
        )

    # DZĒST IERAKSTU

    def delete_record(self):

        if self.selected_id is None:
            messagebox.showwarning(
                "Uzmanību",
                "Vispirms izvēlies ierakstu."
            )
            return

        if not messagebox.askyesno(
            "Dzēst ierakstu",
            f"Vai tiešām dzēst ierakstu ar ID {self.selected_id}?"
        ):
            return

        self.execute_sql(
            f"DELETE FROM {self.current_table} WHERE id = ?",
            [self.selected_id]
        )

    # SQL IZPILDE

    def execute_sql(self, sql, values):

        conn = savienot()

        try:

            conn.execute(sql, values)
            conn.commit()

            self.selected_id = None
            self.clear_form()
            refresh_content(self)

        except sqlite3.IntegrityError as error:

            messagebox.showerror(
                "Datu saistību kļūda",
                "Nevar saglabāt ierakstu.\n\n"
                "Pārbaudi ārējās atslēgas, obligātos laukus "
                "un iespējamos dublikātus.\n\n"
                + str(error)
            )

        except sqlite3.Error as error:

            messagebox.showerror(
                "Datubāzes kļūda",
                str(error)
            )

        finally:
            conn.close()


