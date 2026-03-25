Here is your **AI Document Summarizer Web App** rewritten in the same clean structure and formatting style as the Illegal Buildings project..

----

# AI Document Summarizer Web App.....

A Flask-based AI web application for uploading documents, generating intelligent summaries, and interacting with a contextual chatbot.

---

## Features

* User registration and authentication system
* Upload PDF and TXT documents
* Extractive summarization using NLP techniques
* Abstractive summarization using transformer models
* Context-aware chatbot for document-based Q&A
* Save and manage generated summaries
* RESTful routes for document and summary handling
* Database integration with SQLAlchemy
* Migration support using Flask-Migrate

---

## Prerequisites

* Python 3.9 or higher
* pip (Python package manager)
* Virtual environment (recommended)
* SQLite or MySQL database

---

## Installation

### Clone the repository

```
git clone https://github.com/your-username/ai-document-summarizer.git
cd ai-document-summarizer
```

### Create virtual environment

```
python -m venv venv
venv\Scripts\activate     # Windows
source venv/bin/activate  # macOS/Linux
```

### Install dependencies

```
pip install -r requirements.txt
```

If installing manually:

```
pip install absl-py==2.1.0 alembic==1.14.1 annotated-types==0.7.0 astunparse==1.6.3 bcrypt==4.2.1 blinker==1.9.0 blis==1.2.0 catalogue==2.0.10 certifi==2025.1.31 charset-normalizer==3.4.1 click==8.1.8 cloudpathlib==0.20.0 colorama==0.4.6 confection==0.1.5 cymem==2.0.11 dnspython==2.7.0 email_validator==2.2.0 filelock==3.17.0 Flask==3.1.0 Flask-Bcrypt==1.0.1 Flask-Migrate==4.1.0 Flask-SQLAlchemy==3.1.1 Flask-WTF==1.2.2 flatbuffers==25.1.24 fsspec==2025.2.0 gast==0.6.0 google-pasta==0.2.0 greenlet==3.1.1 grpcio==1.70.0 h5py==3.12.1 huggingface-hub==0.28.1 idna==3.10 itsdangerous==2.2.0 Jinja2==3.1.5 keras==3.8.0 langcodes==3.5.0 language_data==1.3.0 libclang==18.1.1 Mako==1.3.9 marisa-trie==1.2.1 Markdown==3.7 markdown-it-py==3.0.0 MarkupSafe==3.0.2 mdurl==0.1.2 ml-dtypes==0.4.1 murmurhash==1.0.12 namex==0.0.8 numpy==2.0.2 opt_einsum==3.4.0 optree==0.14.0 packaging==24.2 preshed==3.0.9 protobuf==5.29.3 pydantic==2.10.6 pydantic_core==2.27.2 Pygments==2.19.1 PyYAML==6.0.2 regex==2024.11.6 requests==2.32.3 rich==13.9.4 safetensors==0.5.2 shellingham==1.5.4 six==1.17.0 smart-open==7.1.0 spacy==3.8.4 spacy-legacy==3.0.12 spacy-loggers==1.0.5 SQLAlchemy==2.0.37 srsly==2.5.1 tensorboard==2.18.0 tensorboard-data-server==0.7.2 tensorflow==2.18.0 tensorflow-io-gcs-filesystem==0.31.0 tensorflow_intel==2.18.0 termcolor==2.5.0 tf_keras==2.18.0 thinc==8.3.4 tokenizers==0.21.0 tqdm==4.67.1 transformers==4.48.2 typer==0.15.1 typing_extensions==4.12.2 urllib3==2.3.0 wasabi==1.1.3 weasel==0.4.1 Werkzeug==3.1.3 wrapt==1.17.2 WTForms==3.2.1 PyMuPDF==1.23.22
```

Install SpaCy language model:

```
python -m spacy download en_core_web_sm
```

---

### Initialize database

```
flask db init
flask db migrate
flask db upgrade
```

---

### Run the application

```
python app.py
```

---

### Access the application

Open:

```
http://127.0.0.1:5000/
```

---

## Project Structure

```
ai-document-summarizer/
├── app.py
├── requirements.txt
├── migrations/                 # Database migrations
├── instance/                   # Database files
├── static/                     # CSS, JS, assets
├── templates/                  # Jinja2 templates
├── models/                     # Database models
├── routes/                     # Application routes
├── services/                   # AI summarization & chatbot logic
├── utils/                      # Helper functions
└── uploads/                    # Uploaded documents
```

---

## API Routes

### Document Routes

GET /documents - Get all uploaded documents
POST /upload - Upload document
GET /document/{id} - Retrieve document

### Summary Routes

POST /summarize/extractive - Generate extractive summary
POST /summarize/abstractive - Generate abstractive summary

### Chatbot Routes

POST /chat - Ask question based on uploaded document

---

## Frontend

The frontend is built with:

* HTML5 and CSS3
* Jinja2 templating
* Bootstrap (optional styling)
* JavaScript for dynamic interactions

---

## AI Architecture

### Extractive Summarization

* Implemented using SpaCy NLP pipeline
* Sentence scoring based on frequency
* Top-ranked sentence selection

### Abstractive Summarization

* HuggingFace Transformer models
* Deep learning-based text generation
* TensorFlow / Keras backend

### Chatbot

* Transformer-based Question Answering model
* Context retrieval from uploaded document
* Dynamic response generation

---

## Security

* Flask-Login authentication
* Flask-Bcrypt password hashing
* CSRF protection via Flask-WTF
* Secure session management

---

## Contributing

Fork the repository
Create a feature branch (git checkout -b feature/AmazingFeature)
Commit your changes (git commit -m 'Add feature')
Push to the branch (git push origin feature/AmazingFeature)
Open a Pull Request

---

## License

This project is licensed under the MIT License.
