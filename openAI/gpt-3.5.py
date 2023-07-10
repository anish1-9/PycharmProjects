import os
import re
import time
import string
import random
import pdfplumber
import tkinter as tk
import tkinter.font as font
import openai
from tqdm import tqdm
from tkinter import simpledialog, messagebox
from concurrent.futures import ThreadPoolExecutor, as_completed

openai.api_key = os.getenv('OPENAI_API_KEY')
MAX_TOKENS = 4097
OVERLAP = 200


def extract_text(file_path):
    with pdfplumber.open(file_path) as pdf:
        text = ' '.join(page.extract_text().lower() for page in pdf.pages)
    return text


def sanitize_filename(prompt):
    return re.sub(r'[^a-zA-Z0-9_-]', '', prompt.replace(' ', '_'))


class Session:
    def __init__(self):
        self.conversation_history = [{"role": "system", "content": "You are a helpful assistant."}, ]

    def answer_prompt(self, text, prompt):
        def create_responses(chunk):
            conversation_history = [{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": chunk}, {"role": "user", "content": prompt}]
            response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=conversation_history)
            return response['choices'][0]['message']['content'].strip()

        chunks = [text[i:i+MAX_TOKENS] for i in range(0, len(text), MAX_TOKENS-OVERLAP)]
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(create_responses, chunk) for chunk in chunks]
            responses = [future.result() for future in as_completed(futures)]
        return responses[0]


class App:
    def __init__(self, session, file_path):
        self.session = session
        self.text = extract_text(file_path)
        self.root = tk.Tk()
        self.root.geometry("400x300")
        self.root.configure(bg='#FFFFFF')

        self.myFont = font.Font(family='Helvetica', size=14, weight='bold')

        self.label = tk.Label(self.root, text="OpenAI PDF Assistant", bg='#FFFFFF', fg='#000000')
        self.label['font'] = font.Font(size=20, weight='bold')
        self.label.pack(pady=10)

        self.button_ask = tk.Button(self.root, text="Ask", command=self.ask_question, bg='#008CBA', fg='white')
        self.button_ask['font'] = self.myFont
        self.button_ask.pack(pady=10, padx=20, fill='both')

        self.button_summarize = tk.Button(self.root, text="Summarize", command=self.summarize, bg='#008CBA', fg='white')
        self.button_summarize['font'] = self.myFont
        self.button_summarize.pack(pady=10, padx=20, fill='both')

        self.button_exit = tk.Button(self.root, text="Exit", command=self.root.quit, bg='#f44336', fg='white')
        self.button_exit['font'] = self.myFont
        self.button_exit.pack(pady=10, padx=20, fill='both')
        self.button_ask = tk.Button(self.root, text="Ask", command=self.ask_question)
        self.button_summarize = tk.Button(self.root, text="Summarize", command=self.summarize)
        self.button_exit = tk.Button(self.root, text="Exit", command=self.root.quit)
        self.button_ask.pack(fill=tk.X)
        self.button_summarize.pack(fill=tk.X)
        self.button_exit.pack(fill=tk.X)

    def ask_question(self):
        prompt = simpledialog.askstring("Question", "Ask your question:")
        if prompt:
            response = self.session.answer_prompt(self.text, prompt)
            messagebox.showinfo("Response", f"AI's response: {response}")
            file_type = simpledialog.askstring("File Type", "Please enter the desired file type (txt, doc, csv, etc.):")
            filename = sanitize_filename(prompt) + '.' + file_type
            with open(f'output/{filename}', 'w') as f:
                f.write(f'Question: {prompt}\nAI Response: {response}')

    def summarize(self):
        start_time = time.time()
        summary = self.session.answer_prompt(self.text, "Please summarize the text.")
        with open('output_summary.txt', 'w', encoding='utf-8') as f:
            f.write(summary)
        time_taken = time.time() - start_time
        messagebox.showinfo("Summary", f"Summarized text: {summary}\nTime taken: {time_taken:.2f} seconds or {time_taken / 60:.2f} minutes")

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    session = Session()
    app = App(session, r"C:\Users\GF 63\PycharmProjects\pythonProject1\lemh207.pdf")
    app.run()
