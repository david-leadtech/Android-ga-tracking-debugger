# Android GA Tracking Debugger
# Copyright (c) 2025 Alejandro Reinoso
#
# This software is licensed under the Custom Shared-Profit License (CSPL) v1.0.
# See the LICENSE.txt file for details.

__version__ = "1.0.0"

import json
from datetime import datetime, timezone

import tkinter as tk
from tkinter import messagebox, filedialog
import webbrowser

from src.i18n import load_translations, set_language, _
from src.utils import resource_path
from src.log_parser import (
    parse_logging_event_line,
    parse_user_property_line,
    parse_consent_line,
)
from src.config_manager import load_config, save_config
from src.adb_manager import (
    check_adb_installed,
    get_adb_devices,
    LogcatManager,
    AdbError,
)
from src.view import View
from src.model import DataModel


class App:
    def __init__(self, root):
        self.root = root
        self.root.title(f"Analytics Tracking Debugger Android - v{__version__}")
        self.root.iconbitmap(resource_path(
            "./assets/logo-alejandro-reinoso.ico"))

        self.model = DataModel()
        self.logcat_manager = None

        self.config_data = load_config()
        default_lang_code = self.config_data.get("language", "en")
        set_language(default_lang_code)

        self.view = View(self.root, self)
        self.refresh_ui_texts()
        self.refresh_device_combo()
        self.refresh_status_only()
        self._schedule_status_tick()
        self._bind_search_shortcuts()

    def _schedule_status_tick(self):
        self.root.after(2500, self._on_status_timer)

    def _on_status_timer(self):
        self.refresh_device_combo()
        self.refresh_status_only()
        self._schedule_status_tick()

    def _bind_search_shortcuts(self):
        def focus_search(_event=None):
            self.view.search_entry.focus_set()
            self.view.search_entry.select_range(0, tk.END)
            return "break"
        self.root.bind_all("<Control-f>", focus_search)
        self.root.bind_all("<Command-f>", focus_search)

    def refresh_ui_texts(self):
        # Two cascades: 0 = Languages, 1 = Help
        self.view.menubar.entryconfig(0, label=_("menu.languages"))
        self.view.menubar.entryconfig(1, label=_("menu.help"))

        self.view.filemenu.entryconfig(0, label=_("menu.spanish"))
        self.view.filemenu.entryconfig(1, label=_("menu.english"))

        self.view.helpmenu.entryconfig(0, label=_("menu.support"))
        self.view.helpmenu.entryconfig(1, label=_("menu.feedback"))
        self.view.helpmenu.entryconfig(3, label=_("menu.about_me"))

        self.view.start_button.config(text=_("menu.start_log"))
        self.view.stop_button.config(text=_("menu.stop_log"))
        self.view.clear_button.config(text=_("menu.clear_all"))
        self.view.export_button.config(text=_("export.button"))
        self.view.device_label.config(text=_("device.label"))

        self.view.events_title.config(text=_("events.title"))
        self.view.user_props_title.config(text=_("user_props.title"))
        self.view.consent_title.config(text=_("consent.title"))

        self.view.search_label.config(text=_("search.label"))
        self.view.search_button.config(text=_("search.button"))
        self.view.first_button.config(text=_("search.first"))
        self.view.prev_button.config(text=_("search.previous"))
        self.view.next_button.config(text=_("search.next"))
        self.view.last_button.config(text=_("search.last"))
        self.view.jump_button.config(text=_("search.goto_button"))
        self.view.search_goto_label.config(text=_("search.goto_label"))

        self.view.consent_tree.heading("datetime", text=_("consent.datetime"))
        self.view.consent_tree.heading(
            "ad_storage", text=_("consent.ad_storage"))
        self.view.consent_tree.heading("analytics_storage",
                                       text=_("consent.analytics_storage"))
        self.view.consent_tree.heading(
            "ad_user_data", text=_("consent.ad_user_data"))
        self.view.consent_tree.heading("ad_personalization",
                                       text=_("consent.ad_personalization"))
        self.refresh_status_only()

    def refresh_device_combo(self):
        if not check_adb_installed():
            return
        devices = get_adb_devices()
        preferred = self.config_data.get("last_device_serial")
        cur = self.view.get_selected_device_serial()
        if cur and cur in devices:
            preferred = cur
        self.view.set_device_choices(devices, preferred)

    def refresh_status_only(self):
        serial = self.view.get_selected_device_serial()
        capturing = self.logcat_manager is not None
        if not check_adb_installed():
            self.view.set_status_text(_("status.adb.missing"), "#a40000")
            return
        devs = get_adb_devices()
        if not devs:
            self.view.set_status_text(_("status.adb.no_device"), "#8a4b00")
            return
        if serial and serial in devs:
            label = _("status.capturing") if capturing else _("status.ready")
            self.view.set_status_text(f"{label} · {serial}", "#145214")
        else:
            # Selection out of date; first device
            s2 = devs[0]
            self.view.set_status_text(
                (f"{_('status.capturing') if capturing else _('status.ready')} "
                 f"· {s2}"), "#145214",
            )

    def on_device_selected(self):
        serial = self.view.get_selected_device_serial()
        if serial:
            self.config_data["last_device_serial"] = serial
            save_config(self.config_data)
        self.refresh_status_only()

    def on_language_change(self, new_lang):
        set_language(new_lang)
        self.refresh_ui_texts()
        self.config_data["language"] = new_lang
        save_config(self.config_data)

    def handle_adb_error(self, error_type):
        if error_type == AdbError.MULTIPLE_DEVICES:
            messagebox.showerror(_("error.several_devices_title"),
                                 _("error.several_devices_description"))
        self.stop_logging()

    def check_log_queue(self):
        while not self.model.log_queue.empty():
            line = self.model.log_queue.get_nowait()
            self.view.update_console(line + "\n")

            if "Logging event:" in line:
                ev = parse_logging_event_line(line)
                if ev:
                    self.model.add_event(ev)
                    idx = len(self.model.events_data) - 1
                    self.view.insert_event_in_tree(ev, idx)

            up_line = (
                "Setting user property:" in line
                or "Setting user property(FE):" in line
                or "Setting user property (FE):" in line
            )
            if up_line:
                up = parse_user_property_line(line)
                if up:
                    self.model.user_properties[up["name"]] = up["value"]
                    self.view.refresh_user_props_tree(
                        self.model.user_properties)
                    if "non_personalized_ads" in up["name"]:
                        new_consent_state = self.model.current_consent.copy()
                        new_consent_state["datetime"] = up["datetime"]
                        self.model.deduce_ad_personalization(new_consent_state)
                        self._update_consent_view_if_changed(new_consent_state)

            if (
                "Setting storage consent" in line
                or "Setting DMA consent" in line
                or "Setting consent" in line
            ):
                c = parse_consent_line(line)
                if c:
                    self.model.fill_missing_consent_fields(c)
                    self.model.deduce_ad_personalization(c)
                    self._update_consent_view_if_changed(c)

        self.root.after(100, self.check_log_queue)

    def _update_consent_view_if_changed(self, consent_data):
        if self.model.has_consent_changed(consent_data):
            self.model.current_consent.update(consent_data)
            # Export: snapshot of the full merged consent state.
            self.model.append_consent_history(dict(self.model.current_consent))
            new_item_id = self.view.insert_consent_in_tree(
                consent_data, self.model.consent_entries)
            self.model.consent_entries[consent_data["datetime"]] = new_item_id

    def _selected_event_index_from_tree(self, item_id):
        w = self.view.events_tree
        parent = w.parent(item_id) or item_id
        for tag in w.item(parent, "tags"):
            if str(tag).startswith("evidx_"):
                return int(str(tag)[6:])
        return None

    def on_tree_double_click(self, which, event):
        if which == "events":
            w = self.view.events_tree
            iid = w.identify("item", event.x, event.y) or None
            if not iid:
                sel = w.selection()
                if not sel:
                    return
                iid = sel[0]
            idx = self._selected_event_index_from_tree(iid)
            if idx is not None and 0 <= idx < len(self.model.events_data):
                self.view.show_detail_window(
                    _("detail.event_title"),
                    self.model.events_data[idx],
                )
        elif which == "user_props":
            w = self.view.user_props_tree
            iid = w.identify("item", event.x, event.y) or None
            if not iid and w.selection():
                iid = w.selection()[0]
            if not iid:
                return
            text = w.item(iid, "text")
            self.view.show_detail_window(
                _("detail.user_prop_title"), {"line": text})
        elif which == "consent":
            w = self.view.consent_tree
            iid = w.identify("item", event.x, event.y) or None
            if not iid and w.selection():
                iid = w.selection()[0]
            if not iid:
                return
            vals = w.item(iid, "values")
            if not vals or len(vals) < 5:
                return
            data = {
                "datetime": vals[0],
                "ad_storage": vals[1],
                "analytics_storage": vals[2],
                "ad_user_data": vals[3],
                "ad_personalization": vals[4],
            }
            self.view.show_detail_window(_("detail.consent_title"), data)

    def export_session(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[
                ("JSON", "*.json"),
                (_("export.filetype_all"), "*.*"),
            ],
        )
        if not path:
            return
        serial = self.view.get_selected_device_serial()
        payload = {
            "export_version": 1,
            "app_version": __version__,
            "exported_at": datetime.now(timezone.utc).isoformat(),
            "device_serial": serial,
            "events": self.model.events_data,
            "user_properties": self.model.user_properties,
            "consent_history": self.model.consent_history,
        }
        try:
            with open(path, "w", encoding="utf-8") as fh:
                json.dump(payload, fh, ensure_ascii=False, indent=2)
        except OSError as ex:
            messagebox.showerror(_("export.error_title"), str(ex))
            return
        messagebox.showinfo(_("export.success_title"), _("export.success_message"))

    def show_adb_install_dialog(self):
        dialog = tk.Toplevel()
        dialog.title("ADB not found")
        msg_label = tk.Label(dialog, text=_("error.adb_not_found"))
        msg_label.pack(pady=10, padx=10)
        google_button = tk.Button(
            dialog,
            text=_("download_adb"),
            command=lambda: webbrowser.open(
                "https://developer.android.com/tools/releases/platform-tools?hl=es-419"),
        )
        google_button.pack(pady=5)
        close_button = tk.Button(dialog, text=_("close"), command=dialog.destroy)
        close_button.pack(pady=10)

    def show_no_device_dialog(self):
        dialog = tk.Toplevel()
        dialog.title(_("error.device_not_found"))
        msg_label = tk.Label(dialog, text=_("error.no_connected_device"))
        msg_label.pack(pady=10, padx=10)
        close_button = tk.Button(
            dialog, text=_("close"), command=dialog.destroy)
        close_button.pack(pady=10)
        dialog.grab_set()
        dialog.focus_set()

    def start_logging(self):
        if not check_adb_installed():
            self.show_adb_install_dialog()
            return

        self.refresh_device_combo()
        devices = get_adb_devices()
        if not devices:
            self.show_no_device_dialog()
            return

        serial = self.view.get_selected_device_serial()
        if not serial or serial not in devices:
            serial = devices[0]
            self.view.set_device_choices(devices, serial)
        self.config_data["last_device_serial"] = serial
        save_config(self.config_data)

        self.logcat_manager = LogcatManager(
            self.model.log_queue, self.handle_adb_error, device_serial=serial
        )
        self.logcat_manager.start()
        self.check_log_queue()
        self.view.update_console(f"\n--- Start log (device: {serial}) ---\n")
        self.refresh_status_only()

    def stop_logging(self):
        if self.logcat_manager:
            self.logcat_manager.stop()
            self.logcat_manager = None
        self.view.update_console("\n--- Stop log ---\n")
        self.refresh_status_only()

    def clear_all(self):
        self.model.clear_data()
        self.view.clear_ui()

    def search_logs(self):
        self.view.text_area.tag_remove("search_highlight", "1.0", tk.END)
        self.view.text_area.tag_remove("search_current", "1.0", tk.END)
        self.model.search_matches.clear()
        self.model.current_match_index = -1
        term = self.view.search_entry.get().strip()
        if not term:
            self.update_match_label(0, 0)
            return
        start_pos = "1.0"
        while True:
            pos = self.view.text_area.search(term, start_pos, stopindex=tk.END)
            if not pos:
                break
            end_pos = f"{pos}+{len(term)}c"
            self.model.search_matches.append((pos, end_pos))
            self.view.text_area.tag_add("search_highlight", pos, end_pos)
            start_pos = end_pos
        self.view.text_area.tag_config(
            "search_highlight", background="yellow", foreground="black"
        )
        total = len(self.model.search_matches)
        if total > 0:
            self.model.current_match_index = 0
            self.highlight_current_match()
        else:
            self.update_match_label(0, 0)

    def highlight_current_match(self):
        self.view.text_area.tag_remove("search_current", "1.0", tk.END)
        total = len(self.model.search_matches)
        if not (0 <= self.model.current_match_index < total):
            self.update_match_label(0, total)
            return
        start_pos, end_pos = self.model.search_matches[self.model.current_match_index]
        self.view.text_area.tag_add("search_current", start_pos, end_pos)
        self.view.text_area.tag_config(
            "search_current", background="orange", foreground="black"
        )
        self.view.text_area.see(start_pos)
        self.update_match_label(self.model.current_match_index + 1, total)

    def next_match(self):
        if self.model.search_matches and self.model.current_match_index < len(self.model.search_matches) - 1:
            self.model.current_match_index += 1
            self.highlight_current_match()

    def prev_match(self):
        if self.model.search_matches and self.model.current_match_index > 0:
            self.model.current_match_index -= 1
            self.highlight_current_match()

    def jump_to_first(self):
        if self.model.search_matches:
            self.model.current_match_index = 0
            self.highlight_current_match()

    def jump_to_last(self):
        if self.model.search_matches:
            self.model.current_match_index = len(self.model.search_matches) - 1
            self.highlight_current_match()

    def jump_to_index(self):
        if not self.model.search_matches:
            return
        try:
            idx = int(self.view.index_entry.get()) - 1
        except ValueError:
            return
        idx = max(0, min(idx, len(self.model.search_matches) - 1))
        self.model.current_match_index = idx
        self.highlight_current_match()

    def update_match_label(self, current, total):
        self.view.match_label.config(text=f"{current} / {total}")


if __name__ == "__main__":
    load_translations()
    root = tk.Tk()
    app = App(root)
    root.mainloop()
