// document.getElementById("button-collapse-quiz").onclick = () => document.getElementById("button-collapse-quiz").hidden = true;

let button_collapse_quiz = document.getElementById("button-collapse-quiz");
button_collapse_quiz.onclick = () => button_collapse_quiz.hidden = true;

let close_btns = document.getElementsByClassName("close")
for (cb of close_btns) {
    cb.onclick = () => cb.parentElement.hidden = true;
}