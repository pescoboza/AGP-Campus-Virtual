// Hide button from quiz after first click.
let button_collapse_quiz = document.getElementById("button-collapse-quiz");
if (button_collapse_quiz != null){
    button_collapse_quiz.onclick = () => button_collapse_quiz.hidden = true;
}