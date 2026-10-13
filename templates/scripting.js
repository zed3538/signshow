function right() {
    console.log("right");
}

function wrong() {
    console.log("wrong");
}

let question = {text};
let correct = ["I"];
let incorrect = ["hello/goodbye", "Deaf", "man"];

// these are just placeholders for the sake of testing it
// maybe put part above in script to change otherwise make vars for each question

function checkQuestion() {
    if (str===question.correct) {
        right();
    }
    else {
        wrong();
    }
}

// put the script stuff later