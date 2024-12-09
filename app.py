import os
import requests
import PyPDF2
from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

# Groq Cloud API Configuration
API_KEY = "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"
GROQ_COMPLETIONS_ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

# Store PDF text globally for chat
pdf_text = ""


# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    try:
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""


# Split text into chunks for processing
def split_text(text, chunk_size=2000):
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]


# Summarize each section using the Groq Cloud API
def summarize_sections(sections):
    summarized_sections = []
    for section in sections:
        try:
            data = {
                "model": "llama3-8b-8192",
                "messages": [{"role": "user", "content": f"Summarize this text: {section}"}]
            }
            response = requests.post(GROQ_COMPLETIONS_ENDPOINT, headers=HEADERS, json=data)
            response.raise_for_status()
            summary = response.json()["choices"][0]["message"]["content"].strip()

            if "I apologize" not in summary:
                title = summary.split(".")[0][:50] + "..."
                summarized_sections.append({"title": title, "content": summary})
        except Exception as e:
            print(f"Error summarizing section: {e}")
            summarized_sections.append({"title": "Error", "content": "Unable to summarize this section."})
    return summarized_sections


# Generate questions from summaries
def generate_questions(summaries, num_questions=10):
    questions = []
    for idx, summary in enumerate(summaries[:num_questions]):
        try:
            data = {
                "model": "llama3-8b-8192",
                "messages": [
                    {
                        "role": "user",
                        "content": f"Generate a multiple-choice question based on this summary: {summary['content']}"
                    }
                ]
            }
            response = requests.post(GROQ_COMPLETIONS_ENDPOINT, headers=HEADERS, json=data)
            response.raise_for_status()

            raw_question = response.json()["choices"][0]["message"]["content"]

            if "Correct answer:" in raw_question:
                question_part, answer_part = raw_question.split("Correct answer:", 1)
                question_lines = question_part.strip().split("\n")
                options = {
                    "A": "Option A not provided",
                    "B": "Option B not provided",
                    "C": "Option C not provided",
                    "D": "Option D not provided",
                }
                for line in question_lines:
                    if line.startswith("A)"):
                        options["A"] = line[2:].strip()
                    elif line.startswith("B)"):
                        options["B"] = line[2:].strip()
                    elif line.startswith("C)"):
                        options["C"] = line[2:].strip()
                    elif line.startswith("D)"):
                        options["D"] = line[2:].strip()

                questions.append({
                    "question": f"Question {idx + 1}: {question_lines[0].strip()}",
                    "options": options,
                    "answer": f"Answer: {answer_part.strip()}",
                })
            else:
                questions.append({
                    "question": f"Question {idx + 1}: {raw_question.strip()}",
                    "options": {
                        "A": "Option A not provided",
                        "B": "Option B not provided",
                        "C": "Option C not provided",
                        "D": "Option D not provided",
                    },
                    "answer": "Answer: Not provided",
                })
        except Exception as e:
            print(f"Error generating question: {e}")
            questions.append({
                "question": f"Question {idx + 1}: Error generating this question.",
                "options": {
                    "A": "Option A not available",
                    "B": "Option B not available",
                    "C": "Option C not available",
                    "D": "Option D not available",
                },
                "answer": "Answer: N/A",
            })
    return questions


# Chat with PDF
@app.route('/chat', methods=['POST'])
def chat():
    global pdf_text
    user_query = request.json.get("query")
    if not user_query:
        return jsonify({"response": "Please ask a valid question."})

    try:
        data = {
            "model": "llama3-8b-8192",
            "messages": [
                {"role": "user", "content": f"Based on this PDF content: {pdf_text}. Answer this query: {user_query}"}
            ]
        }
        response = requests.post(GROQ_COMPLETIONS_ENDPOINT, headers=HEADERS, json=data)
        response.raise_for_status()
        chat_response = response.json()["choices"][0]["message"]["content"].strip()
        return jsonify({"response": chat_response})
    except Exception as e:
        print(f"Error in chat response: {e}")
        return jsonify({"response": "An error occurred while processing your question. Please try again."})


# Upload and process PDF
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    global pdf_text

    if 'pdf' not in request.files:
        return redirect(url_for('home'))

    file = request.files['pdf']
    if file.filename == '':
        return redirect(url_for('home'))

    save_path = os.path.join("uploads", file.filename)
    os.makedirs("uploads", exist_ok=True)
    file.save(save_path)

    pdf_text = extract_text_from_pdf(save_path)
    if not pdf_text:
        return "Error: Could not extract text from the uploaded PDF."

    sections = split_text(pdf_text)
    summaries = summarize_sections(sections)
    questions = generate_questions(summaries)

    return render_template('result.html', summaries=summaries, questions=questions)


if __name__ == '__main__':
    app.run(debug=True)
