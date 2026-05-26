from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)


# AI QUESTION GENERATOR 

def generate_ai_questions():

    question_bank = [

        # DIRECT QUESTIONS
        {"type": "direct", "question": "What is Python?", "answer": "programming language"},
        {"type": "direct", "question": "Who developed Python?", "answer": "Guido van Rossum"},
        {"type": "direct", "question": "What keyword defines a function in Python?", "answer": "def"},
        {"type": "direct", "question": "What data type is True/False?", "answer": "bool"},
        {"type": "direct", "question": "What is 2 + 3 in Python?", "answer": "5"},
        {"type": "direct", "question": "What is the extension of Python file?", "answer": ".py"},
        {"type": "direct", "question": "What is input function used for?", "answer": "taking input"},
        {"type": "direct", "question": "What loop is used in Python?", "answer": "for loop"},
        {"type": "direct", "question": "What symbol is used for comments?", "answer": "#"},
        {"type": "direct", "question": "What does AI stand for?", "answer": "artificial intelligence"},

        # MCQ QUESTIONS
        {
            "type": "mcq",
            "question": "Which is a Python framework?",
            "options": ["A. Django", "B. React", "C. Laravel", "D. Angular"],
            "answer": "A"
        },
        {
            "type": "mcq",
            "question": "Which file extension is Python?",
            "options": ["A. .java", "B. .py", "C. .html", "D. .css"],
            "answer": "B"
        },
        {
            "type": "mcq",
            "question": "Which keyword is used for function?",
            "options": ["A. func", "B. define", "C. def", "D. function"],
            "answer": "C"
        },
        {
            "type": "mcq",
            "question": "Which is mutable type?",
            "options": ["A. tuple", "B. string", "C. list", "D. int"],
            "answer": "C"
        },
        {
            "type": "mcq",
            "question": "Which is used to print output?",
            "options": ["A. echo", "B. print", "C. show", "D. display"],
            "answer": "B"
        }
    ]

    # Shuffle and pick only 10 questions
    random.shuffle(question_bank)
    return question_bank[:10]


quiz_data = []

# ROUTES

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/get_quiz")
def get_quiz():

    global quiz_data
    quiz_data = generate_ai_questions()

    return jsonify(quiz_data)


@app.route("/submit", methods=["POST"])
def submit():

    data = request.json
    answers = data["answers"]

    score = 0

    for i, q in enumerate(quiz_data):

        user_ans = answers[i].strip().lower()
        correct_ans = q["answer"].strip().lower()

        if user_ans == correct_ans:
            score += 1

    total = len(quiz_data)

    percentage = (score / total) * 100

    # GRADE SYSTEM
    
    if percentage >= 80:
        grade = "A+ 🏆"
    elif percentage >= 60:
        grade = "B 👍"
    elif percentage >= 40:
        grade = "C 🙂"
    else:
        grade = "Fail ❌"

    return jsonify({
        "score": score,
        "total": total,
        "percentage": round(percentage, 2),
        "grade": grade
    })

# RUN APP

if __name__ == "__main__":
    app.run(debug=True)