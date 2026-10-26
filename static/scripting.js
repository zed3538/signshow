function right() {
    alert("Correct!");
    window.location.href = '/learn/new-question';
}

function wrong() {
    alert("Incorrect!")
}

function checkQuestion(event) {
    console.log(event.target);
    if (event.target.classList.contains('correct')) {
        right();
    }
    else {
        wrong();
    }
}