import concurrent.futures
import os
import threading
import time
import openai
from tqdm import tqdm, trange
import PyPDF2

# Set constants
openai.api_key = os.getenv('OPENAI_API_KEY')
pdf_path = r"C:\Users\GF 63\PycharmProjects\pythonProject1\lemh207.pdf"
output_folder = r"C:\Users\GF 63\PycharmProjects\pythonProject1\output"
os.makedirs(output_folder, exist_ok=True)

def input_with_timeout(prompt, timeout):
    user_input = None

    def get_input():
        nonlocal user_input
        user_input = input(prompt)

    timer = threading.Timer(timeout, get_input)
    try:
        timer.start()
        while user_input is None:
            pass
        return user_input
    except KeyboardInterrupt:
        return None
    finally:
        timer.cancel()

def extract_text_from_pdf_page(pdf_reader, page_num):
    try:
        page = pdf_reader.pages[page_num]
        return page.extract_text()
    except KeyError as e:
        print(f"Error occurred on page {page_num}: {type(e).__name__}")
        print(f"Skipping page {page_num} due to error: {str(e)}")
        return ""
    except Exception as e:
        print(f"Error occurred on page {page_num}: {type(e).__name__}")
        print(f"Error details: {str(e)}")
        return ""

with open(pdf_path, "rb") as pdf_file:
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    num_pages = len(list(pdf_reader.pages))  # Convert to a regular list
    summary = ""

    with concurrent.futures.ThreadPoolExecutor() as executor:
        page_nums = list(range(num_pages))
        progress_bar = tqdm(total=len(page_nums), desc="Summarizing Pages",
                            bar_format="{l_bar}{bar:100} | Elapsed: {elapsed} | Remaining: {remaining}",
                            ncols=100)
        start_time = time.time()
        color_map = trange(101, bar_format='{l_bar}{bar:100}', ncols=100)
        futures = {executor.submit(extract_text_from_pdf_page, pdf_reader, page_num): page_num for page_num in page_nums}

        for future in concurrent.futures.as_completed(futures):
            page_num = futures[future]
            try:
                summary += str(future.result()) + "\n"
            except Exception as e:
                print(f"Error occurred on page {page_num}: {type(e).__name__}")
                print(f"Error details: {str(e)}")
            progress_bar.update(1)
            color_map.update(1)
            progress_bar.set_postfix(color=color_map)

        with open(os.path.join(output_folder, "output_summary.txt"), "w", encoding='utf-8') as summary_file:
            summary_file.write(summary)
        elapsed_time = time.time() - start_time
        print("Summary:\n", summary, f"\nTime taken to run the PDF: {elapsed_time:.2f} seconds")

while True:
    prompt = input_with_timeout("Enter a prompt (or 'stop' to finish): ", 60)
    if not prompt or prompt.lower() == 'stop':
        break
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                            messages=[{"role": "user", "content": summary}])["choices"][0][
        "message"]["content"]

    with open(os.path.join(output_folder, prompt + ".txt"), "w", encoding='utf-8') as file:
        file.write(response)
        print("Response:\n", response)

# Wait for user input to keep the console active
input("Press Enter to exit...")

