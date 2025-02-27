function submitAnswers() {
    const answers = {};
    const passages = document.querySelectorAll('.passage');
    passages.forEach((passage, index) => {
        const textarea = passage.querySelector('textarea');
        answers[index] = textarea.value;
    });

    fetch('/submit', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(answers),
    })
    .then(response => response.json())
    .then(data => {
        const resultDiv = document.getElementById('result');
        resultDiv.innerHTML = `<h2>你的得分: ${data.total_score}</h2>`;
        data.results.forEach(result => {
            resultDiv.innerHTML += `
                <div>
                    <h3>${result.passage_title}</h3>
                    <p>正确答案: ${result.correct_answer}</p>
                    <p>你的答案: ${result.user_answer}</p>
                    <p>得分: ${result.score}</p>
                </div>
            `;
        });
    });
}