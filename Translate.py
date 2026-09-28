import os
import tkinter as tk
from tkinter import messagebox, ttk
import translators as ts


class LanguageTranslatorApp:

    def __init__(self, root):
        self.root = root
        self.root.title("CodeAlpha - Language Translation Tool")
        self.root.geometry("650x550")
        self.root.configure(bg="#f4f6f9")

        # Supported languages dictionary
        self.languages = {
            "English": "en", "Spanish": "es", "French": "fr",
            "German": "de", "Italian": "it", "Chinese": "zh",
            "Arabic": "ar", "Hindi": "hi", "Japanese": "ja", "Russian": "ru"
        }

        self.setup_ui()

    def setup_ui(self):
        # Header Styling
        header_frame = tk.Frame(self.root, bg="#1e293b", height=70)
        header_frame.pack(fill="x")
        header_label = tk.Label(header_frame, text="Language Translation Tool", fg="white", bg="#1e293b", font=("Arial", 16, "bold"))
        header_label.pack(pady=20)

        # Main container
        main_frame = tk.Frame(self.root, bg="#f4f6f9")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # --- Source Language Section ---
        src_label_frame = tk.Frame(main_frame, bg="#f4f6f9")
        src_label_frame.pack(fill="x", pady=(0, 5))
        tk.Label(src_label_frame, text="Source Language:", font=("Arial", 10, "bold"), bg="#f4f6f9", fg="#334155").pack(side="left")

        self.src_lang_cb = ttk.Combobox(src_label_frame, values=["Auto-Detect"] + list(self.languages.keys()), state="readonly", width=20)
        self.src_lang_cb.set("Auto-Detect")
        self.src_lang_cb.pack(side="left", padx=10)

        self.src_text = tk.Text(main_frame, height=6, font=("Arial", 11), wrap="word", bd=1, relief="solid")
        self.src_text.pack(fill="x", pady=(0, 15))

        # --- Target Language Section ---
        tgt_label_frame = tk.Frame(main_frame, bg="#f4f6f9")
        tgt_label_frame.pack(fill="x", pady=(0, 5))
        tk.Label(tgt_label_frame, text="Target Language:", font=("Arial", 10, "bold"), bg="#f4f6f9", fg="#334155").pack(side="left")

        self.tgt_lang_cb = ttk.Combobox(tgt_label_frame, values=list(self.languages.keys()), state="readonly", width=20)
        self.tgt_lang_cb.set("Spanish")
        self.tgt_lang_cb.pack(side="left", padx=10)

        self.tgt_text = tk.Text(main_frame, height=6, font=("Arial", 11), wrap="word", bd=1, relief="solid", bg="#f8fafc")
        self.tgt_text.pack(fill="x", pady=(0, 15))

        # --- Control Buttons ---
        btn_frame = tk.Frame(main_frame, bg="#f4f6f9")
        btn_frame.pack(fill="x", pady=10)

        # Translate Button
        translate_btn = tk.Button(btn_frame, text="Translate Text", bg="#2563eb", fg="white", font=("Arial", 11, "bold"),
                                  activebackground="#1d4ed8", activeforeground="white", bd=0, padx=15, pady=8, command=self.translate_text)
        translate_btn.pack(side="left", padx=(0, 10))

        # Copy Button
        copy_btn = tk.Button(btn_frame, text="📋 Copy", bg="#64748b", fg="white", font=("Arial", 10),
                             activebackground="#475569", activeforeground="white", bd=0, padx=10, pady=6, command=self.copy_to_clipboard)
        copy_btn.pack(side="left", padx=5)

        # Listen Button
        listen_btn = tk.Button(btn_frame, text="🔊 Listen", bg="#10b981", fg="white", font=("Arial", 10),
                               activebackground="#059669", activeforeground="white", bd=0, padx=10, pady=6, command=self.text_to_speech)
        listen_btn.pack(side="left", padx=5)

        # Clear Button
        clear_btn = tk.Button(btn_frame, text="Clear", bg="#ef4444", fg="white", font=("Arial", 10),
                              activebackground="#dc2626", activeforeground="white", bd=0, padx=10, pady=6, command=self.clear_fields)
        clear_btn.pack(side="right")

    def translate_text(self):
        text_to_translate = self.src_text.get("1.0", tk.END).strip()
        if not text_to_translate:
            messagebox.showwarning("Input Error", "Please enter some text to translate.")
            return

        src_lang = self.src_lang_cb.get()
        tgt_lang = self.tgt_lang_cb.get()

        src_code = "auto" if src_lang == "Auto-Detect" else self.languages[src_lang]
        tgt_code = self.languages[tgt_lang]

        try:
            translated = ts.translate_text(text_to_translate, from_language=src_code, to_language=tgt_code, translator='google')
            self.tgt_text.delete("1.0", tk.END)
            self.tgt_text.insert(tk.END, translated)
        except Exception as e:
            messagebox.showerror("Translation Error", f"Connection failed: {str(e)}")

    def copy_to_clipboard(self):
        translated_text = self.tgt_text.get("1.0", tk.END).strip()
        if translated_text:
            self.root.clipboard_clear()
            self.root.clipboard_append(translated_text)
            messagebox.showinfo("Success", "Translated text copied to clipboard!")
        else:
            messagebox.showwarning("Empty Field", "There is no text to copy.")

    def text_to_speech(self):
        translated_text = self.tgt_text.get("1.0", tk.END).strip()
        if not translated_text:
            messagebox.showwarning("Empty Field", "There is no text to read aloud.")
            return

        # Uses native Windows built-in speech engine directly without imports to clear the warning
        try:
            clean_text = translated_text.replace('"', '""')
            os.system(f'mshta vbscript:Execute("CreateObject(""SAPI.SpVoice"").Speak(""{clean_text}"")(window.close)")')
        except Exception as e:
            messagebox.showerror("Audio Error", f"Built-in voice system busy: {str(e)}")

    def clear_fields(self):
        self.src_text.delete("1.0", tk.END)
        self.tgt_text.delete("1.0", tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = LanguageTranslatorApp(root)
    root.mainloop()
