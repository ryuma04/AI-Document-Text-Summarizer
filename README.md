📄 AI Document Summarizer Web App

An AI-powered web application that allows users to upload documents (PDF/TXT), generate summaries using extractive and abstractive techniques, 
and interact with a chatbot to ask questions based on the uploaded document.

🚀 Features

🔐 User Registration & Login (Authentication System)

📂 Upload PDF and TXT documents

📝 Extractive Summarization

🤖 Abstractive Summarization (Transformer-based)

💬 Chatbot Q&A based on uploaded document

💾 Save and manage generated summaries

🗄 Database integration using SQLAlchemy

🔄 Migration support using Flask-Migrate

🛠 Tech Stack

Backend: Flask

Database: SQLite / MySQL (via SQLAlchemy)

Authentication: Flask-Login + Flask-Bcrypt
AI Models: Transformers (HuggingFace), SpaCy


📦 Required Python Packages

Install all dependencies using:

pip install -r requirements.txt

Or manually install using:

pip install absl-py==2.1.0 alembic==1.14.1 annotated-types==0.7.0 astunparse==1.6.3 bcrypt==4.2.1 blinker==1.9.0 blis==1.2.0 catalogue==2.0.10 certifi==2025.1.31 charset-normalizer==3.4.1 click==8.1.8 cloudpathlib==0.20.0 colorama==0.4.6 confection==0.1.5 cymem==2.0.11 dnspython==2.7.0 email_validator==2.2.0 filelock==3.17.0 Flask==3.1.0 Flask-Bcrypt==1.0.1 Flask-Migrate==4.1.0 Flask-SQLAlchemy==3.1.1 Flask-WTF==1.2.2 flatbuffers==25.1.24 fsspec==2025.2.0 gast==0.6.0 google-pasta==0.2.0 greenlet==3.1.1 grpcio==1.70.0 h5py==3.12.1 huggingface-hub==0.28.1 idna==3.10 itsdangerous==2.2.0 Jinja2==3.1.5 keras==3.8.0 langcodes==3.5.0 language_data==1.3.0 libclang==18.1.1 Mako==1.3.9 marisa-trie==1.2.1 Markdown==3.7 markdown-it-py==3.0.0 MarkupSafe==3.0.2 mdurl==0.1.2 ml-dtypes==0.4.1 murmurhash==1.0.12 namex==0.0.8 numpy==2.0.2 opt_einsum==3.4.0 optree==0.14.0 packaging==24.2 preshed==3.0.9 protobuf==5.29.3 pydantic==2.10.6 pydantic_core==2.27.2 Pygments==2.19.1 PyYAML==6.0.2 regex==2024.11.6 requests==2.32.3 rich==13.9.4 safetensors==0.5.2 shellingham==1.5.4 six==1.17.0 smart-open==7.1.0 spacy==3.8.4 spacy-legacy==3.0.12 spacy-loggers==1.0.5 SQLAlchemy==2.0.37 srsly==2.5.1 tensorboard==2.18.0 tensorboard-data-server==0.7.2 tensorflow==2.18.0 tensorflow-io-gcs-filesystem==0.31.0 tensorflow_intel==2.18.0 termcolor==2.5.0 tf_keras==2.18.0 thinc==8.3.4 tokenizers==0.21.0 tqdm==4.67.1 transformers==4.48.2 typer==0.15.1 typing_extensions==4.12.2 urllib3==2.3.0 wasabi==1.1.3 weasel==0.4.1 Werkzeug==3.1.3 wrapt==1.17.2 WTForms==3.2.1 PyMuPDF==1.23.22

Additionally, install the SpaCy language model:

python -m spacy download en_core_web_sm
⚙️ Project Setup
1️⃣ Clone the Repository
git clone https://github.com/your-username/ai-document-summarizer.git
cd ai-document-summarizer
2️⃣ Create Virtual Environment
python -m venv venv
venv\Scripts\activate   # Windows
3️⃣ Install Dependencies
pip install -r requirements.txt
4️⃣ Initialize Database
flask db init
flask db migrate
flask db upgrade
5️⃣ Run Application
python app.py

Server will run on:

http://127.0.0.1:5000/
🧠 How It Works
📌 Extractive Summarization

Uses SpaCy NLP pipeline

Scores sentences based on frequency and importance

Selects top-ranked sentences

📌 Abstractive Summarization

Uses HuggingFace Transformer models

Generates new summarized text using deep learning

📌 Chatbot

Processes uploaded document text

Uses transformer-based QA model

Generates contextual answers based on document

📂 Supported File Types

.pdf

.txt

🔒 Authentication System

Password hashing using Flask-Bcrypt

Secure session handling

Form validation via Flask-WTF

🧩 Future Improvements

Role-based user dashboar

Deep Learning: TensorFlow / Keras

PDF Processing: PyMuPDF

Frontend: HTML, CSS, Jinja2 Templates
