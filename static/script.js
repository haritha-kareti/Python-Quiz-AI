let quizData = [];
let currentIndex = 0;
let answers = [];

// LOAD QUIZ
fetch("/get_quiz")
.then(res => res.json())
.then(data => {
    quizData = data;
    answers = new Array(quizData.length).fill("");
    showQuestion();
});

function showQuestion() {

    let q = quizData[currentIndex];

    let html = `<h2>Q${currentIndex + 1}. ${q.question}</h2>`;

    // DIRECT QUESTION
    if (q.type === "direct") {

        html += `<input type="text" id="ans" value="${answers[currentIndex]}" placeholder="Type your answer">`;
    }

    // MCQ QUESTION
    else {

        q.options.forEach(opt => {

            let checked = answers[currentIndex] === opt[0] ? "checked" : "";

            html += `
            <label class="option">
                <input type="radio" name="mcq" value="${opt[0]}" ${checked}>
                ${opt}
            </label>`;
        });
    }

    document.getElementById("quiz-box").innerHTML = html;
}


// SAVE ANSWER
function saveAnswer() {

    let q = quizData[currentIndex];

    if (q.type === "direct") {
        answers[currentIndex] = document.getElementById("ans").value;
    } else {
        let selected = document.querySelector('input[name="mcq"]:checked');
        answers[currentIndex] = selected ? selected.value : "";
    }
}


// NEXT QUESTION
function nextQuestion() {

    saveAnswer();

    if (currentIndex < quizData.length - 1) {
        currentIndex++;
        showQuestion();
    }
}


// PREVIOUS QUESTION
function prevQuestion() {

    saveAnswer();

    if (currentIndex > 0) {
        currentIndex--;
        showQuestion();
    }
}


// SUBMIT QUIZ
function submitQuiz() {

    saveAnswer();

    fetch("/submit", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({answers})
    })
    .then(res => res.json())
    .then(data => {

        document.getElementById("result").innerHTML =
            ` Score: ${data.score}/${data.total}<br>
              Percentage: ${data.percentage}%<br>
              Grade: ${data.grade}`;
    });
}