function right() {
    console.log("right");
}

function wrong() {
    console.log("wrong");
}

console.log("Scripts loaded")
function checkQuestion(event) {
    console.log(event.target);
    if (event.target.classList.contains('correct')) {
        right();
    }
    else {
        wrong();
    }
}