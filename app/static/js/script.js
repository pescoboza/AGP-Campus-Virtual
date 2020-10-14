// Hide button from quiz after first click.
let button_collapse_quiz = document.getElementById("button-collapse-quiz");
button_collapse_quiz.onclick = () => button_collapse_quiz.hidden = true;


function hideParent(e) {
    let ele = e.target;
    ele.parentElement.hidden = true;
}

// Hide flashed messages when clicking on cross.
let flashes = document.getElementsByClassName("aler");
let num_flashes = flashes.length;
for (let i = 0; i < num_flashes; i++) {
    flashes[i].addEventListener("click", hideParent);
}