let question = {text};
correct = [];
incorrect = [, , , ];

function right() {
    console.log("right");
}

function wrong() {
    console.log("wrong");
}

function checkQuestion() {
    if (str===question.correct) {
        right()
    }
    else {
        wrong()
    }
}
