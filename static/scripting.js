function right() {
    console.log("right");
}

function wrong() {
    console.log("wrong");
}

let question = "What does this sign mean?";
let correct = ["I"];
let incorrect = ["hello/goodbye", "Deaf", "man"];

// these are just placeholders for the sake of testing it
// maybe put part above in script to change otherwise make vars for each question
console.log("Scrpits loaded")
function checkQuestion(event) {
    // let buttonClicked = event.target
    if (event.target.classList.contains('correct')) {
        right();
    }
    else {
        wrong();
    }
}

// put the script stuff later