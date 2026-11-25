"""R.A.Z.A. 2.0 - Rapid Algorithmic Zone Analyzer & Cryptanalysis Suite.
Cyberpunk-themed unified GUI for Dictionary Attacks, Hash Generation, and Caesar Analysis.
"""

from __future__ import annotations
import os
import time
import threading
import tkinter as tk
from tkinter import messagebox, filedialog
from typing import Optional

from ..caesar import encrypt, decrypt, crack_caesar, ALPHABET
from ..hashing import generate_all_hashes, SUPPORTED_ALGORITHMS
from ..cracker import DictionaryCracker, DEFAULT_WORDLIST

BG_DARK = "#0a0a0a"
BG_PANEL = "#111111"
FG_GREEN = "#00ff00"
FG_DARK_GREEN = "#00aa00"
FG_MUTED = "#007700"
FG_WHITE = "#ffffff"
BG_ACTIVE = "#003300"
FONT_TITLE = ("Consolas", 24, "bold")
FONT_SUBTITLE = ("Consolas", 10)
FONT_HEADING = ("Consolas", 12, "bold")
FONT_BODY = ("Consolas", 10)
FONT_CODE = ("Consolas", 10)
FONT_STAT = ("Consolas", 11, "bold")


class RazaApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("R.A.Z.A. 2.0 - Kryptoanalyse Suite")
        self.geometry("820x660")
        self.minsize(760, 600)
        self.configure(bg=BG_DARK)

        self.cracker = DictionaryCracker()
        self.current_wordlist = DEFAULT_WORDLIST
        self.crack_stop_event: Optional[threading.Event] = None
        self.crack_thread: Optional[threading.Thread] = None

        self._build_header()
        self._build_tab_bar()

        # Container für Tab-Inhalte
        self.tab_container = tk.Frame(self, bg=BG_DARK)
        self.tab_container.pack(fill="both", expand=True, padx=20, pady=(10, 20))

        # Frames für Tabs
        self.tab_dict = tk.Frame(self.tab_container, bg=BG_DARK)
        self.tab_hash = tk.Frame(self.tab_container, bg=BG_DARK)
        self.tab_caesar = tk.Frame(self.tab_container, bg=BG_DARK)

        self._build_dict_tab()
        self._build_hash_tab()
        self._build_caesar_tab()

        # Standard-Tab aktivieren
        self.switch_tab("dict")

    # --------------------------------------------------
    # Header & Tab Navigation
    # --------------------------------------------------

    def _build_header(self) -> None:
        header_frame = tk.Frame(self, bg=BG_DARK)
        header_frame.pack(fill="x", pady=(15, 5))

        title = tk.Label(
            header_frame,
            text="R . A . Z . A .  2 . 0",
            font=FONT_TITLE,
            bg=BG_DARK,
            fg=FG_GREEN
        )
        title.pack()

        subtitle = tk.Label(
            header_frame,
            text="RAPID ALGORITHMIC ZONE ANALYZER // KRYPTOANALYSE-SUITE",
            font=FONT_SUBTITLE,
            bg=BG_DARK,
            fg=FG_DARK_GREEN
        )
        subtitle.pack(pady=(2, 0))

    def _build_tab_bar(self) -> None:
        bar = tk.Frame(self, bg=BG_DARK)
        bar.pack(fill="x", padx=20, pady=(10, 5))

        self.tab_buttons: dict[str, tk.Button] = {}

        tabs = [
            ("dict", "[ ⚡ WÖRTERBUCH-ANGRIFF ]"),
            ("hash", "[ 🔑 HASH-GENERATOR ]"),
            ("caesar", "[ 🏛️ CAESAR-KRYPTOANALYSE ]"),
        ]

        for tab_id, tab_label in tabs:
            btn = tk.Button(
                bar,
                text=tab_label,
                font=FONT_HEADING,
                bg=BG_PANEL,
                fg=FG_GREEN,
                activebackground=FG_GREEN,
                activeforeground=BG_DARK,
                relief="solid",
                bd=1,
                cursor="hand2",
                command=lambda tid=tab_id: self.switch_tab(tid),
                padx=12,
                pady=6
            )
            btn.pack(side="left", padx=4, expand=True, fill="x")
            self.tab_buttons[tab_id] = btn

    def switch_tab(self, active_tab: str) -> None:
        # Hide all frames
        self.tab_dict.pack_forget()
        self.tab_hash.pack_forget()
        self.tab_caesar.pack_forget()

        # Update button styles
        for tid, btn in self.tab_buttons.items():
            if tid == active_tab:
                btn.config(bg=FG_GREEN, fg=BG_DARK, relief="sunken")
            else:
                btn.config(bg=BG_PANEL, fg=FG_GREEN, relief="solid")

        # Show selected tab
        if active_tab == "dict":
            self.tab_dict.pack(fill="both", expand=True)
        elif active_tab == "hash":
            self.tab_hash.pack(fill="both", expand=True)
        elif active_tab == "caesar":
            self.tab_caesar.pack(fill="both", expand=True)

    # --------------------------------------------------
    # Tab 1: Wörterbuch-Angriff
    # --------------------------------------------------

    def _build_dict_tab(self) -> None:
        # Hash Input Section
        input_frame = tk.LabelFrame(
            self.tab_dict,
            text=" [ ZIEL-HASH KONFIGURATION ] ",
            font=FONT_BODY,
            bg=BG_DARK,
            fg=FG_DARK_GREEN,
            bd=1,
            relief="solid"
        )
        input_frame.pack(fill="x", pady=10, padx=5, ipady=5)

        row1 = tk.Frame(input_frame, bg=BG_DARK)
        row1.pack(fill="x", padx=10, pady=5)

        tk.Label(
            row1,
            text="> HASH:",
            font=FONT_CODE,
            bg=BG_DARK,
            fg=FG_GREEN
        ).pack(side="left", padx=(0, 5))

        self.dict_hash_entry = tk.Entry(
            row1,
            font=FONT_CODE,
            bg=BG_PANEL,
            fg=FG_GREEN,
            insertbackground=FG_GREEN,
            relief="solid",
            bd=1,
            highlightthickness=1,
            highlightbackground=FG_DARK_GREEN,
            highlightcolor=FG_GREEN
        )
        self.dict_hash_entry.pack(side="left", fill="x", expand=True, padx=5)

        # Algo selector
        tk.Label(
            row1,
            text="ALGO:",
            font=FONT_CODE,
            bg=BG_DARK,
            fg=FG_GREEN
        ).pack(side="left", padx=(10, 5))

        self.dict_algo_var = tk.StringVar(value="sha1")
        algo_menu = tk.OptionMenu(
            row1,
            self.dict_algo_var,
            "sha1",
            "sha256",
            "md5"
        )
        algo_menu.config(
            bg=BG_PANEL,
            fg=FG_GREEN,
            activebackground=BG_ACTIVE,
            activeforeground=FG_GREEN,
            font=FONT_CODE,
            relief="solid",
            bd=1,
            highlightthickness=0
        )
        algo_menu["menu"].config(bg=BG_PANEL, fg=FG_GREEN, font=FONT_CODE)
        algo_menu.pack(side="left")

        # Wordlist Selector Row
        row2 = tk.Frame(input_frame, bg=BG_DARK)
        row2.pack(fill="x", padx=10, pady=5)

        tk.Label(
            row2,
            text="> WORTE:",
            font=FONT_CODE,
            bg=BG_DARK,
            fg=FG_GREEN
        ).pack(side="left", padx=(0, 5))

        self.wordlist_label = tk.Label(
            row2,
            text=os.path.basename(self.current_wordlist),
            font=FONT_CODE,
            bg=BG_PANEL,
            fg=FG_DARK_GREEN,
            anchor="w",
            relief="solid",
            bd=1,
            padx=5
        )
        self.wordlist_label.pack(side="left", fill="x", expand=True, padx=5)

        browse_btn = tk.Button(
            row2,
            text="DATEI WÄHLEN...",
            font=FONT_CODE,
            bg=BG_PANEL,
            fg=FG_GREEN,
            relief="solid",
            bd=1,
            cursor="hand2",
            command=self._select_wordlist
        )
        browse_btn.pack(side="left")

        # Controls & Action
        ctrl_frame = tk.Frame(self.tab_dict, bg=BG_DARK)
        ctrl_frame.pack(fill="x", pady=10)

        self.btn_crack_start = tk.Button(
            ctrl_frame,
            text="[ ANGRIFF STARTEN ]",
            font=FONT_HEADING,
            bg=BG_PANEL,
            fg=FG_GREEN,
            activebackground=FG_GREEN,
            activeforeground=BG_DARK,
            relief="solid",
            bd=1,
            cursor="hand2",
            command=self.start_dict_attack,
            pady=8
        )
        self.btn_crack_start.pack(side="left", expand=True, fill="x", padx=(0, 5))

        self.btn_crack_stop = tk.Button(
            ctrl_frame,
            text="[ ABBRECHEN ]",
            font=FONT_HEADING,
            bg=BG_PANEL,
            fg="#ff4444",
            activebackground="#ff4444",
            activeforeground=BG_DARK,
            relief="solid",
            bd=1,
            cursor="hand2",
            state="disabled",
            command=self.stop_dict_attack,
            pady=8
        )
        self.btn_crack_stop.pack(side="left", expand=True, fill="x", padx=(5, 0))

        # Status & Telemetry Frame
        stats_frame = tk.LabelFrame(
            self.tab_dict,
            text=" [ TELEMETRIE & FORTSCHRITT ] ",
            font=FONT_BODY,
            bg=BG_DARK,
            fg=FG_DARK_GREEN,
            bd=1,
            relief="solid"
        )
        stats_frame.pack(fill="x", pady=5, padx=5, ipady=5)

        self.dict_status_label = tk.Label(
            stats_frame,
            text="> STATUS: BEREIT_",
            font=FONT_STAT,
            bg=BG_DARK,
            fg=FG_GREEN,
            anchor="w"
        )
        self.dict_status_label.pack(fill="x", padx=10, pady=2)

        self.dict_progress_label = tk.Label(
            stats_frame,
            text="> GEPRÜFT: 0 PASSWÖRTER",
            font=FONT_STAT,
            bg=BG_DARK,
            fg=FG_GREEN,
            anchor="w"
        )
        self.dict_progress_label.pack(fill="x", padx=10, pady=2)

        self.dict_speed_label = tk.Label(
            stats_frame,
            text="> GESCHWINDIGKEIT: 0 PASSWÖRTER/S",
            font=FONT_STAT,
            bg=BG_DARK,
            fg=FG_GREEN,
            anchor="w"
        )
        self.dict_speed_label.pack(fill="x", padx=10, pady=2)

        self.dict_time_label = tk.Label(
            stats_frame,
            text="> DAUER: 0.0s",
            font=FONT_STAT,
            bg=BG_DARK,
            fg=FG_GREEN,
            anchor="w"
        )
        self.dict_time_label.pack(fill="x", padx=10, pady=2)

        # Output result banner
        res_frame = tk.LabelFrame(
            self.tab_dict,
            text=" [ ERGEBNIS ] ",
            font=FONT_BODY,
            bg=BG_DARK,
            fg=FG_DARK_GREEN,
            bd=1,
            relief="solid"
        )
        res_frame.pack(fill="both", expand=True, pady=10, padx=5)

        self.dict_result_label = tk.Label(
            res_frame,
            text="> NOCH KEINE PRÜFUNG DURCHGEFÜHRT_",
            font=FONT_HEADING,
            bg=BG_PANEL,
            fg=FG_GREEN,
            relief="solid",
            bd=1,
            wraplength=700,
            pady=15
        )
        self.dict_result_label.pack(fill="both", expand=True, padx=10, pady=10)

    def _select_wordlist(self) -> None:
        selected = filedialog.askopenfilename(
            title="Wortliste auswählen",
            filetypes=[("Textdateien", "*.txt"), ("Alle Dateien", "*.*")]
        )
        if selected:
            self.current_wordlist = selected
            self.wordlist_label.config(text=os.path.basename(selected))

    def start_dict_attack(self) -> None:
        target = self.dict_hash_entry.get().strip()
        if not target:
            messagebox.showerror("FEHLER", "Bitte einen Ziel-Hash eingeben.")
            return

        algo = self.dict_algo_var.get()
        self.crack_stop_event = threading.Event()

        self.btn_crack_start.config(state="disabled")
        self.btn_crack_stop.config(state="normal")
        self.dict_status_label.config(text="> STATUS: PRÜFUNG LÄUFT...", fg=FG_GREEN)
        self.dict_result_label.config(text="> SUCHE PASSWORT IN WORTLISTE...", fg=FG_GREEN)

        self.crack_thread = threading.Thread(
            target=self._run_crack_thread,
            args=(target, algo, self.current_wordlist, self.crack_stop_event),
            daemon=True
        )
        self.crack_thread.start()

    def stop_dict_attack(self) -> None:
        if self.crack_stop_event:
            self.crack_stop_event.set()
            self.dict_status_label.config(text="> STATUS: ABBRUCH WIRD ANGEFORDERT...", fg="#ffaa00")

    def _run_crack_thread(
        self,
        target_hash: str,
        algo: str,
        wordlist_path: str,
        stop_event: threading.Event
    ) -> None:
        def on_progress(checked: int, speed: float, elapsed: float) -> None:
            self.after(0, self._update_dict_gui_progress, checked, speed, elapsed)

        result = self.cracker.crack(
            target_hash=target_hash,
            algorithm=algo,
            wordlist_path=wordlist_path,
            progress_callback=on_progress,
            stop_event=stop_event
        )

        self.after(0, self._on_crack_complete, result)

    def _update_dict_gui_progress(self, checked: int, speed: float, elapsed: float) -> None:
        self.dict_progress_label.config(text=f"> GEPRÜFT: {checked:,.0f} PASSWÖRTER".replace(",", "'"))
        self.dict_speed_label.config(text=f"> GESCHWINDIGKEIT: {speed:,.0f} PASSWÖRTER/S".replace(",", "'"))
        self.dict_time_label.config(text=f"> DAUER: {elapsed:.1f}s")

    def _on_crack_complete(self, result: dict) -> None:
        self.btn_crack_start.config(state="normal")
        self.btn_crack_stop.config(state="disabled")

        self._update_dict_gui_progress(result["checked"], result["speed"], result["elapsed"])

        if result["found"]:
            msg = f"> [TREFFER!] PASSWORT GEFUNDEN: {result['password']}"
            self.dict_result_label.config(text=msg, fg=FG_GREEN)
            self.dict_status_label.config(text="> STATUS: ERFOLGREICH GEKNACKT!", fg=FG_GREEN)
        else:
            self.dict_result_label.config(text=f"> {result['message']}", fg="#ffaa00")
            self.dict_status_label.config(text="> STATUS: ABGESCHLOSSEN (KEIN TREFFER)", fg="#ffaa00")

    # --------------------------------------------------
    # Tab 2: Hash-Generator
    # --------------------------------------------------

    def _build_hash_tab(self) -> None:
        frame = tk.LabelFrame(
            self.tab_hash,
            text=" [ HASH-BERECHNUNG AUS KLARTEXT ] ",
            font=FONT_BODY,
            bg=BG_DARK,
            fg=FG_DARK_GREEN,
            bd=1,
            relief="solid"
        )
        frame.pack(fill="both", expand=True, padx=5, pady=10, ipady=10)

        # Input Row
        tk.Label(
            frame,
            text="> KLARTEXT-WORT ODER PASSWORT EINGEBEN:",
            font=FONT_HEADING,
            bg=BG_DARK,
            fg=FG_GREEN
        ).pack(anchor="w", padx=15, pady=(10, 5))

        self.hash_input_entry = tk.Entry(
            frame,
            font=FONT_CODE,
            bg=BG_PANEL,
            fg=FG_GREEN,
            insertbackground=FG_GREEN,
            relief="solid",
            bd=1,
            highlightthickness=1,
            highlightbackground=FG_DARK_GREEN,
            highlightcolor=FG_GREEN
        )
        self.hash_input_entry.pack(fill="x", padx=15, pady=5)
        self.hash_input_entry.bind("<KeyRelease>", lambda e: self._calculate_hashes())

        btn_row = tk.Frame(frame, bg=BG_DARK)
        btn_row.pack(fill="x", padx=15, pady=8)

        calc_btn = tk.Button(
            btn_row,
            text="[ HASHES BERECHNEN ]",
            font=FONT_BODY,
            bg=BG_PANEL,
            fg=FG_GREEN,
            activebackground=FG_GREEN,
            activeforeground=BG_DARK,
            relief="solid",
            bd=1,
            cursor="hand2",
            command=self._calculate_hashes
        )
        calc_btn.pack(side="left")

        # Results Display
        self.hash_labels: dict[str, tk.Entry] = {}

        algos = [("SHA-1", "sha1"), ("SHA-256", "sha256"), ("MD5", "md5")]
        for display_name, algo_key in algos:
            algo_box = tk.Frame(frame, bg=BG_DARK)
            algo_box.pack(fill="x", padx=15, pady=6)

            tk.Label(
                algo_box,
                text=f"{display_name}:",
                font=FONT_STAT,
                bg=BG_DARK,
                fg=FG_GREEN,
                width=10,
                anchor="w"
            ).pack(side="left")

            entry = tk.Entry(
                algo_box,
                font=FONT_CODE,
                bg=BG_PANEL,
                fg=FG_GREEN,
                relief="solid",
                bd=1,
                readonlybackground=BG_PANEL
            )
            entry.pack(side="left", fill="x", expand=True, padx=5)
            self.hash_labels[algo_key] = entry

            copy_btn = tk.Button(
                algo_box,
                text="KOPIEREN",
                font=FONT_CODE,
                bg=BG_PANEL,
                fg=FG_DARK_GREEN,
                activebackground=FG_GREEN,
                activeforeground=BG_DARK,
                relief="solid",
                bd=1,
                cursor="hand2",
                command=lambda k=algo_key: self._copy_hash(k)
            )
            copy_btn.pack(side="left", padx=2)

            use_btn = tk.Button(
                algo_box,
                text="➡ WÖRTERBUCH",
                font=FONT_CODE,
                bg=BG_PANEL,
                fg=FG_GREEN,
                activebackground=FG_GREEN,
                activeforeground=BG_DARK,
                relief="solid",
                bd=1,
                cursor="hand2",
                command=lambda k=algo_key: self._transfer_to_dictionary(k)
            )
            use_btn.pack(side="left", padx=2)

    def _calculate_hashes(self) -> None:
        text = self.hash_input_entry.get().strip()
        if not text:
            for entry in self.hash_labels.values():
                entry.delete(0, tk.END)
            return

        hashes = generate_all_hashes(text)
        for k, h in hashes.items():
            entry = self.hash_labels[k]
            entry.delete(0, tk.END)
            entry.insert(0, h)

    def _copy_hash(self, algo_key: str) -> None:
        val = self.hash_labels[algo_key].get().strip()
        if val:
            self.clipboard_clear()
            self.clipboard_append(val)
            messagebox.showinfo("KOPIERT", f"{algo_key.upper()}-Hash in die Zwischenablage kopiert!")

    def _transfer_to_dictionary(self, algo_key: str) -> None:
        val = self.hash_labels[algo_key].get().strip()
        if not val:
            self._calculate_hashes()
            val = self.hash_labels[algo_key].get().strip()
        if not val:
            messagebox.showwarning("HINWEIS", "Bitte zuerst ein Wort eingeben.")
            return

        # Ins Wörterbuch-Tab übernehmen
        self.dict_hash_entry.delete(0, tk.END)
        self.dict_hash_entry.insert(0, val)
        self.dict_algo_var.set(algo_key)
        self.switch_tab("dict")

    # --------------------------------------------------
    # Tab 3: Caesar-Kryptoanalyse
    # --------------------------------------------------

    def _build_caesar_tab(self) -> None:
        # Auto-Cracker Section
        auto_frame = tk.LabelFrame(
            self.tab_caesar,
            text=" [ AUTOMATISCHER ANGRIFF & WÖRTER-MATCHING ] ",
            font=FONT_BODY,
            bg=BG_DARK,
            fg=FG_DARK_GREEN,
            bd=1,
            relief="solid"
        )
        auto_frame.pack(fill="x", padx=5, pady=8, ipady=5)

        tk.Label(
            auto_frame,
            text="> GEHEIMTEXT EINGEBEN:",
            font=FONT_CODE,
            bg=BG_DARK,
            fg=FG_GREEN
        ).pack(anchor="w", padx=10, pady=(5, 2))

        self.caesar_cipher_entry = tk.Entry(
            auto_frame,
            font=FONT_CODE,
            bg=BG_PANEL,
            fg=FG_GREEN,
            insertbackground=FG_GREEN,
            relief="solid",
            bd=1,
            highlightthickness=1,
            highlightbackground=FG_DARK_GREEN,
            highlightcolor=FG_GREEN
        )
        self.caesar_cipher_entry.pack(fill="x", padx=10, pady=5)
        # Klassenbeispiel vorbefüllen
        default_challenge = "JXLQLSLJV UHVHQW ZDWHU, PDFDTXHV GLVOLNH VRBEHDQV"
        self.caesar_cipher_entry.insert(0, default_challenge)

        btn_row = tk.Frame(auto_frame, bg=BG_DARK)
        btn_row.pack(fill="x", padx=10, pady=5)

        crack_btn = tk.Button(
            btn_row,
            text="[ AUTOMATISCH ENTSCHLÜSSELN ]",
            font=FONT_HEADING,
            bg=BG_PANEL,
            fg=FG_GREEN,
            activebackground=FG_GREEN,
            activeforeground=BG_DARK,
            relief="solid",
            bd=1,
            cursor="hand2",
            command=self._run_caesar_crack,
            pady=4
        )
        crack_btn.pack(side="left", padx=(0, 5))

        demo_btn = tk.Button(
            btn_row,
            text="DEMO-TEXT LADEN",
            font=FONT_CODE,
            bg=BG_PANEL,
            fg=FG_DARK_GREEN,
            activebackground=FG_GREEN,
            activeforeground=BG_DARK,
            relief="solid",
            bd=1,
            cursor="hand2",
            command=lambda: (
                self.caesar_cipher_entry.delete(0, tk.END),
                self.caesar_cipher_entry.insert(0, default_challenge)
            )
        )
        demo_btn.pack(side="left")

        # Results area
        self.caesar_result_box = tk.Label(
            auto_frame,
            text="> BEREIT FÜR CAESAR-ANALYSE_",
            font=FONT_CODE,
            bg=BG_PANEL,
            fg=FG_GREEN,
            relief="solid",
            bd=1,
            justify="left",
            anchor="w",
            padx=10,
            pady=10
        )
        self.caesar_result_box.pack(fill="x", padx=10, pady=8)

        # Manual Tool Section
        man_frame = tk.LabelFrame(
            self.tab_caesar,
            text=" [ MANUELLES VER- & ENTSCHLÜSSELN MIT SCHLÜSSEL ] ",
            font=FONT_BODY,
            bg=BG_DARK,
            fg=FG_DARK_GREEN,
            bd=1,
            relief="solid"
        )
        man_frame.pack(fill="both", expand=True, padx=5, pady=8, ipady=5)

        slider_row = tk.Frame(man_frame, bg=BG_DARK)
        slider_row.pack(fill="x", padx=10, pady=5)

        tk.Label(
            slider_row,
            text="SCHLÜSSEL (0 - 25):",
            font=FONT_CODE,
            bg=BG_DARK,
            fg=FG_GREEN
        ).pack(side="left", padx=(0, 10))

        self.caesar_key_var = tk.IntVar(value=3)
        self.caesar_slider = tk.Scale(
            slider_row,
            from_=0,
            to=25,
            orient="horizontal",
            variable=self.caesar_key_var,
            bg=BG_DARK,
            fg=FG_GREEN,
            troughcolor=BG_PANEL,
            highlightthickness=0,
            font=FONT_CODE,
            length=300
        )
        self.caesar_slider.pack(side="left", fill="x", expand=True)

        text_row = tk.Frame(man_frame, bg=BG_DARK)
        text_row.pack(fill="x", padx=10, pady=5)

        tk.Label(
            text_row,
            text="TEXT:",
            font=FONT_CODE,
            bg=BG_DARK,
            fg=FG_GREEN
        ).pack(side="left", padx=(0, 5))

        self.caesar_manual_input = tk.Entry(
            text_row,
            font=FONT_CODE,
            bg=BG_PANEL,
            fg=FG_GREEN,
            insertbackground=FG_GREEN,
            relief="solid",
            bd=1,
            highlightthickness=1,
            highlightbackground=FG_DARK_GREEN,
            highlightcolor=FG_GREEN
        )
        self.caesar_manual_input.pack(side="left", fill="x", expand=True, padx=5)

        m_btn_row = tk.Frame(man_frame, bg=BG_DARK)
        m_btn_row.pack(fill="x", padx=10, pady=5)

        enc_btn = tk.Button(
            m_btn_row,
            text="[ VERSCHLÜSSELN (+KEY) ]",
            font=FONT_CODE,
            bg=BG_PANEL,
            fg=FG_GREEN,
            relief="solid",
            bd=1,
            cursor="hand2",
            command=self._manual_encrypt
        )
        enc_btn.pack(side="left", padx=(0, 5))

        dec_btn = tk.Button(
            m_btn_row,
            text="[ ENTSCHLÜSSELN (-KEY) ]",
            font=FONT_CODE,
            bg=BG_PANEL,
            fg=FG_GREEN,
            relief="solid",
            bd=1,
            cursor="hand2",
            command=self._manual_decrypt
        )
        dec_btn.pack(side="left")

        self.caesar_manual_out = tk.Label(
            man_frame,
            text="",
            font=FONT_CODE,
            bg=BG_PANEL,
            fg=FG_GREEN,
            relief="solid",
            bd=1,
            anchor="w",
            padx=10,
            pady=8
        )
        self.caesar_manual_out.pack(fill="x", padx=10, pady=5)

    def _run_caesar_crack(self) -> None:
        text = self.caesar_cipher_entry.get().strip()
        if not text:
            messagebox.showerror("FEHLER", "Bitte einen Geheimtext eingeben.")
            return

        results = crack_caesar(text)
        best = results[0]
        words_found = ", ".join(best["matched_words"]) if best["matched_words"] else "Keine Wörterliste-Treffer"

        display_text = (
            f"> ERGEBNIS DER KRYPTOANALYSE:\n"
            f"  Bester Schlüssel:  {best['key']} (Verschiebung um {best['key']} Positionen)\n"
            f"  Trefferpunkte:     {best['score']} Wörter gefunden ({words_found})\n"
            f"  Klartext:          {best['text']}\n\n"
            f"> NÄCHSTE KANDIDATEN:\n"
            f"  #2: Key {results[1]['key']:02d} (Score {results[1]['score']}) -> {results[1]['text'][:45]}...\n"
            f"  #3: Key {results[2]['key']:02d} (Score {results[2]['score']}) -> {results[2]['text'][:45]}..."
        )
        self.caesar_result_box.config(text=display_text)

    def _manual_encrypt(self) -> None:
        text = self.caesar_manual_input.get().strip()
        key = self.caesar_key_var.get()
        out = encrypt(text, key)
        self.caesar_manual_out.config(text=f"> VERSCHLÜSSELT (Key {key}): {out}")

    def _manual_decrypt(self) -> None:
        text = self.caesar_manual_input.get().strip()
        key = self.caesar_key_var.get()
        out = decrypt(text, key)
        self.caesar_manual_out.config(text=f"> ENTSCHLÜSSELT (Key {key}): {out}")


def run_app() -> None:
    app = RazaApp()
    app.mainloop()


if __name__ == "__main__":
    run_app()
