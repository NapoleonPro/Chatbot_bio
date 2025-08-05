from flask import Flask, render_template, request
from llm import ask_gemini

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# 💬 Tangani pertanyaan dari form
@app.route('/chat', methods=['POST'])
def chat():
    user_question = request.form['question'].strip()
    if not user_question:
        return render_template('index.html', response="Pertanyaannya kosong.")
    
    response = ask_gemini(user_question)
    return render_template('index.html', response=response)

if __name__ == '__main__':
    app.run(debug=True)
