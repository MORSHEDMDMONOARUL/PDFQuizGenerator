PDF Quiz Generator with Chat Feature
A web-based application that allows users to upload PDF files, generate professional summaries, create multiple-choice questions, and chat with the PDF content. This project is built with Flask, integrates Groq Cloud API, and uses a simple and user-friendly interface.

Features
Upload PDF: Upload any PDF file to extract its content.
Professional Summarization: Generate concise and professional summaries of the PDF content.
Question Generation: Create multiple-choice questions (MCQs) based on the summaries.
Chat with PDF: Interact with the PDF content through a chatbot interface. Ask questions, and get relevant answers dynamically.
User-Friendly Interface: Modern, responsive design for easy navigation and interaction.



Installation
git clone https://github.com/your-repo/pdf-quiz-generator.git
cd pdf-quiz-generator

Create a Virtual Environment:
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

Install Dependencies:
pip install -r requirements.txt

Set Up Groq Cloud API:
Obtain an API key from Groq Cloud.
Replace the API_KEY variable in app.py with your Groq Cloud API key.

Run the Application:
python app.py


Access the Application: Open your browser and visit:
http://127.0.0.1:5000/


Usage
Upload a PDF:

Go to the home page and upload a PDF file.
View Summaries and Questions:

After uploading, view the automatically generated summaries and MCQs.
Chat with the PDF:

Use the chatbox to ask questions about the uploaded PDF content.
Repeat:

Upload another PDF or refine your interactions with the chat feature.


Requirements
Python: 3.7 or higher
Flask: Web framework
PyPDF2: PDF text extraction
Groq Cloud API: For summarization, question generation, and chatbot functionality
Bootstrap: For styling the interface




""I will add images later""





Future Improvements
Add support for additional languages.
Enhance question generation quality using advanced models.
Implement persistent chat history across sessions.
Provide downloadable summaries and quizzes in PDF format.

Contributing
We welcome contributions! Feel free to fork this repository and submit a pull request. For major changes, please open an issue first to discuss the changes.

License
This project is licensed under the MIT License. See the LICENSE file for details.

Acknowledgments
Groq Cloud API for enabling summarization and chat functionalities.
Flask Framework for simplifying web application development.
Bootstrap for a modern and responsive UI design.