from flask import render_template, url_for, flash, redirect, request, session, jsonify
from app import app, db, bcrypt
from app.forms import SubmitTextForm, RegistrationForm, LoginForm
from app.summarizer import Summarizer, nlp
from app.models import User, Summary
from transformers import pipeline
import os
import fitz  # PyMuPDF
from werkzeug.utils import secure_filename

qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")

# Initialize summarizer once at module level (avoids reloading models per request)
summarizer = Summarizer(nlp)

ALLOWED_EXTENSIONS = {'txt', 'pdf'}
UPLOAD_FOLDER = "uploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text.strip()

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(email=form.email.data, password=hashed_password, age=form.age.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session['user_id'] = user.email
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login unsuccessful. Please check email and password.', 'danger')
    return render_template('login.html', form=form)

@app.route("/logout")
def logout():
    session.pop('user_id', None)
    session.pop('summary_type', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

@app.route('/index', methods=['GET', 'POST'])
def index():
    global summarizer
    form = SubmitTextForm(size=600)
    
    if form.validate_on_submit():
        text = request.form['text']
        num_sentences = 5
        summary_type = request.form['summary_type']
        session['summary_type'] = summary_type

        file = request.files.get('file')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            ext = filename.rsplit('.', 1)[1].lower()
            if ext == 'txt':
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read().strip()
            elif ext == 'pdf':
                text = extract_text_from_pdf(file_path)

        if not text:
            flash("Please enter text or upload a file.", "danger")
            return redirect(url_for('index'))

        if summary_type == 'extractive':
            word_weights, sentence_weights, sents, summary = summarizer.summarize_text(text, num_sentences)
        elif summary_type == 'abstractive':
            word_weights, sentence_weights, sents, summary = summarizer.abstractive_summarize(text, num_sentences)
        elif summary_type == 'hybrid':
            word_weights, sentence_weights, sents, summary = summarizer.hybrid_summarize(text, num_sentences)

        top_five_words = sorted(word_weights, key=word_weights.get, reverse=True)[:5] if word_weights else []
        sentence_weights = [value for key, value in sentence_weights.items()] if sentence_weights else []
        weighted_sentence_weights = [value / max(sentence_weights) for value in sentence_weights] if sentence_weights else []
        sentences_with_weights = list(zip(sents, weighted_sentence_weights)) if sents else []

        return render_template('summary.html', text=summary, top_words=top_five_words, sentence_weights=sentence_weights, sents=sentences_with_weights)

    return render_template('home.html', text='', form=form)

@app.route('/summary')
def summary():
    return render_template('summary.html')

@app.route('/save_summary', methods=['POST'])
def save_summary():
    edited_summary = request.form['edited_summary']
    e = session['user_id']
    s_type = session['summary_type']
    new_summary = Summary(email=e, summary_content=edited_summary, summary_type=s_type)
    db.session.add(new_summary)
    db.session.commit()
    flash('Your summary has been saved successfully!')
    return redirect(url_for('index'))

def chatbot_response(user_input):
    if 'user_id' not in session:
        return "Please log in and generate a summary first."

    user_email = session['user_id']
    latest_summary = Summary.query.filter_by(email=user_email).order_by(Summary.id.desc()).first()

    if not latest_summary:
        return "You haven't generated a summary yet. Please generate one first!"

    context = latest_summary.summary_content
    result = qa_pipeline(question=user_input, context=context)
    return result['answer']

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if 'user_id' not in session:
        flash("Please log in first.", "danger")
        return redirect(url_for('login'))

    user_email = session['user_id']
    summaries = Summary.query.filter_by(email=user_email).order_by(Summary.id.desc()).all()
    
    selected_summary_content = summaries[0].summary_content if summaries else "No summaries available. Please generate one first."

    if request.method == 'POST':
        user_input = request.json.get('user_input')
        selected_summary_id = request.json.get('summary_id')
        
        if not selected_summary_id:
            return jsonify({'response': "Please select a summary before asking a question."})

        selected_summary = Summary.query.filter_by(id=selected_summary_id, email=user_email).first()
        
        if not selected_summary:
            return jsonify({'response': "Invalid summary selection."})
        
        result = qa_pipeline(question=user_input, context=selected_summary.summary_content)
        return jsonify({'response': result['answer']})

    return render_template('chat.html', summaries=summaries, selected_summary_content=selected_summary_content)
