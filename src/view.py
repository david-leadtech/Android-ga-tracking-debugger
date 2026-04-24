# Android GA Tracking Debugger
# Copyright (c) 2025 Alejandro Reinoso
#
# This software is licensed under the Custom Shared-Profit License (CSPL) v1.0.
# See the LICENSE.txt file for details.

import json
import sys
import tkinter as tk
from tkinter import scrolledtext, ttk, Menu
import webbrowser

from src.i18n import _


def _apply_ttk_style():
    style = ttk.Style()
    try:
        if sys.platform == "darwin":
            style.theme_use("aqua")
        elif sys.platform == "win32":
            style.theme_use("vista")
        else:
            style.theme_use("clam")
    except tk.TclError:
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass


class View:
    def __init__(self, root, controller):
        self._root = root
        self.controller = controller
        _apply_ttk_style()

        main_paned = tk.PanedWindow(
            root, orient=tk.VERTICAL, sashwidth=8, sashrelief="raised")
        main_paned.pack(fill=tk.BOTH, expand=True)

        # --- MENU: Languages, Help ---
        self.menubar = Menu(root)
        root.config(menu=self.menubar)

        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label=_("menu.spanish"),
                                  command=lambda: self.controller.on_language_change("es"))
        self.filemenu.add_command(label=_("menu.english"),
                                  command=lambda: self.controller.on_language_change("en"))

        self.helpmenu = Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label=_("menu.support"),
                                  command=lambda: webbrowser.open("https://alejandroreinoso.com/contacto/?utm_source=ga_android_debugger&utm_medium=ga_android_debugger&utm_term=support"))
        self.helpmenu.add_command(label=_("menu.feedback"),
                                  command=lambda: webbrowser.open("https://alejandroreinoso.com/contacto/?utm_source=ga_android_debugger&utm_medium=ga_android_debugger&utm_term=feedback"))
        self.helpmenu.add_separator()
        self.helpmenu.add_command(label=_("menu.about_me"),
                                  command=lambda: webbrowser.open("https://www.linkedin.com/in/alejandroreinosogomez/"))

        self.menubar.add_cascade(label=_("menu.languages"), menu=self.filemenu)
        self.menubar.add_cascade(label=_("menu.help"), menu=self.helpmenu)

        # Top: actions, export, device selector, status
        top_frame = tk.Frame(main_paned, bd=2, relief="groove")
        main_paned.add(top_frame, minsize=56)

        btn_row = tk.Frame(top_frame)
        btn_row.pack(fill=tk.X, padx=8, pady=6)

        self.start_button = tk.Button(
            btn_row, text=_("menu.start_log"),
            command=self.controller.start_logging)
        self.start_button.pack(side=tk.LEFT, padx=3)

        self.stop_button = tk.Button(
            btn_row, text=_("menu.stop_log"),
            command=self.controller.stop_logging)
        self.stop_button.pack(side=tk.LEFT, padx=3)

        self.clear_button = tk.Button(
            btn_row, text=_("menu.clear_all"),
            command=self.controller.clear_all)
        self.clear_button.pack(side=tk.LEFT, padx=3)

        self.export_button = tk.Button(
            btn_row, text=_("export.button"),
            command=self.controller.export_session)
        self.export_button.pack(side=tk.LEFT, padx=(12, 3))

        self.status_label = tk.Label(
            btn_row, text="", anchor="w", fg="#1a5f1a", width=42)
        self.status_label.pack(side=tk.RIGHT, padx=6)

        dev_frame = tk.Frame(btn_row)
        dev_frame.pack(side=tk.RIGHT, padx=8)
        self.device_label = tk.Label(dev_frame, text=_("device.label"))
        self.device_label.pack(side=tk.LEFT, padx=(0, 6))
        self.device_combo = ttk.Combobox(
            dev_frame, width=28, state="readonly")
        self.device_combo.pack(side=tk.LEFT)
        self.device_combo.bind(
            "<<ComboboxSelected>>", lambda _e: self.controller.on_device_selected())

        # --- INTERMEDIATE FRAME -> subdiv (izq, der) ---
        middle_frame = tk.Frame(main_paned, bd=2, relief="groove")
        main_paned.add(middle_frame, minsize=150)

        left_frame = tk.Frame(middle_frame, bg="white")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.user_props_title = tk.Label(
            left_frame, text=_("user_props.title"), bg="white")
        self.user_props_title.pack(anchor="w", pady=(0, 2))

        up_container = tk.Frame(left_frame)
        up_container.pack(fill=tk.BOTH, expand=True)
        up_scrollbar = ttk.Scrollbar(up_container, orient=tk.VERTICAL)
        self.user_props_tree = ttk.Treeview(
            up_container, yscrollcommand=up_scrollbar.set)
        up_scrollbar.config(command=self.user_props_tree.yview)
        up_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.user_props_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.consent_title = tk.Label(
            left_frame, text=_("consent.title"), bg="white")
        self.consent_title.pack(anchor="w", pady=(5, 2))

        consent_container = tk.Frame(left_frame)
        consent_container.pack(fill=tk.BOTH, expand=True)
        consent_scrollbar = ttk.Scrollbar(
            consent_container, orient=tk.VERTICAL)
        self.consent_tree = ttk.Treeview(
            consent_container,
            columns=("datetime", "ad_storage", "analytics_storage",
                     "ad_user_data", "ad_personalization"),
            show="headings",
            yscrollcommand=consent_scrollbar.set,
        )
        consent_scrollbar.config(command=self.consent_tree.yview)
        consent_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.consent_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.consent_tree.column("datetime", width=130)
        self.consent_tree.column("ad_storage", width=90)
        self.consent_tree.column("analytics_storage", width=120)
        self.consent_tree.column("ad_user_data", width=120)
        self.consent_tree.column("ad_personalization", width=130)

        right_frame = tk.Frame(middle_frame, bg="white")
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.events_title = tk.Label(
            right_frame, text=_("events.title"), bg="white")
        self.events_title.pack(anchor="w")

        events_container = tk.Frame(right_frame)
        events_container.pack(fill=tk.BOTH, expand=True)
        events_scrollbar = ttk.Scrollbar(events_container, orient=tk.VERTICAL)
        self.events_tree = ttk.Treeview(
            events_container, yscrollcommand=events_scrollbar.set)
        events_scrollbar.config(command=self.events_tree.yview)
        events_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.events_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.events_tree.bind(
            "<Double-1>", lambda e: self.controller.on_tree_double_click("events", e))
        self.user_props_tree.bind(
            "<Double-1>", lambda e: self.controller.on_tree_double_click("user_props", e))
        self.consent_tree.bind(
            "<Double-1>", lambda e: self.controller.on_tree_double_click("consent", e))

        # --- LOWER FRAME -> console + search
        bottom_frame = tk.Frame(main_paned, bd=2, relief="sunken")
        main_paned.add(bottom_frame, minsize=50)

        frame_search = tk.Frame(bottom_frame)
        frame_search.pack(pady=5, fill=tk.X)

        self.search_label = tk.Label(frame_search, text=_("search.label"))
        self.search_label.pack(side=tk.LEFT)
        self.search_entry = tk.Entry(frame_search, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)

        self.search_button = tk.Button(
            frame_search, text=_("search.button"),
            command=self.controller.search_logs)
        self.search_button.pack(side=tk.LEFT, padx=5)

        self.first_button = tk.Button(
            frame_search, text="|<<", command=self.controller.jump_to_first)
        self.first_button.pack(side=tk.LEFT, padx=2)

        self.prev_button = tk.Button(
            frame_search, text="<<", command=self.controller.prev_match)
        self.prev_button.pack(side=tk.LEFT, padx=2)

        self.match_label = tk.Label(frame_search, text="0 / 0")
        self.match_label.pack(side=tk.LEFT, padx=10)

        self.next_button = tk.Button(
            frame_search, text=">>", command=self.controller.next_match)
        self.next_button.pack(side=tk.LEFT, padx=2)

        self.last_button = tk.Button(
            frame_search, text=">>|", command=self.controller.jump_to_last)
        self.last_button.pack(side=tk.LEFT, padx=2)

        self.search_goto_label = tk.Label(
            frame_search, text=_("search.goto_label"))
        self.search_goto_label.pack(side=tk.LEFT, padx=5)
        self.index_entry = tk.Entry(frame_search, width=5)
        self.index_entry.pack(side=tk.LEFT)
        self.jump_button = tk.Button(
            frame_search, text=_("search.goto_button"),
            command=self.controller.jump_to_index)
        self.jump_button.pack(side=tk.LEFT, padx=5)

        self.text_area = scrolledtext.ScrolledText(
            bottom_frame, width=100, height=10)
        self.text_area.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

    def set_status_text(self, text, color="#1a5f1a"):
        self.status_label.config(text=text, fg=color)

    def get_selected_device_serial(self):
        s = self.device_combo.get().strip()
        return s if s else None

    def set_device_choices(self, serials, preferred_serial=None):
        self.device_combo["values"] = serials
        if not serials:
            self.device_combo.set("")
            return
        if preferred_serial and preferred_serial in serials:
            self.device_combo.set(preferred_serial)
        else:
            self.device_combo.set(serials[0])

    def show_detail_window(self, title, payload):
        win = tk.Toplevel(self._root)
        win.title(title)
        win.geometry("640x400")
        mono = ("Menlo", 12) if sys.platform == "darwin" else (
            ("Consolas", 10) if sys.platform == "win32" else ("Monospace", 11)
        )
        ta = scrolledtext.ScrolledText(win, wrap=tk.WORD, font=mono)
        ta.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        if isinstance(payload, (dict, list)):
            text = json.dumps(payload, ensure_ascii=False, indent=2)
        else:
            text = str(payload)
        ta.insert("1.0", text)
        ta.config(state=tk.DISABLED)
        tk.Button(win, text=_("close"), command=win.destroy).pack(pady=6)

    def update_console(self, text):
        self.text_area.insert(tk.END, text)
        self.text_area.see(tk.END)

    def insert_event_in_tree(self, ev, event_index):
        """Inserts an event; event_index is used to open the same object from the model on double-click."""
        dt = ev["datetime"]
        name = ev["name"]
        params = ev["params"]
        tag = f"evidx_{event_index}"
        parent_id = self.events_tree.insert(
            "", tk.END, text=f"{dt} - {name}", tags=(tag,))
        for k, v in params.items():
            self.events_tree.insert(
                parent_id, tk.END, text=f"{k} = {v}", tags=(tag,))
        self.events_tree.see(parent_id)

    def insert_consent_in_tree(self, cdict, consent_entries_from_model):
        dt = cdict["datetime"]
        values = (
            dt,
            cdict.get("ad_storage", ""),
            cdict.get("analytics_storage", ""),
            cdict.get("ad_user_data", ""),
            cdict.get("ad_personalization", ""),
        )
        if dt in consent_entries_from_model:
            self.consent_tree.delete(consent_entries_from_model[dt])

        new_item = self.consent_tree.insert("", tk.END, values=values)
        self.consent_tree.see(new_item)

        return new_item

    def refresh_user_props_tree(self, user_properties_from_model):
        for item in self.user_props_tree.get_children():
            self.user_props_tree.delete(item)
        for prop_name, prop_val in user_properties_from_model.items():
            self.user_props_tree.insert(
                "", tk.END, text=f"{prop_name} = {prop_val}")
        children = self.user_props_tree.get_children()
        if children:
            self.user_props_tree.see(children[-1])

    def clear_ui(self):
        self.text_area.delete("1.0", tk.END)
        for tree in [self.events_tree, self.user_props_tree, self.consent_tree]:
            for item in tree.get_children():
                tree.delete(item)
