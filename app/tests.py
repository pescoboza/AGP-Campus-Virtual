#########################################################################
# Test for module model
#########################################################################

from flask import render_template

from app import main
from app.models import MultipleChoiceQuestion, MultipleChoiceQuiz, Module

def create_module(name="Test Module",num_questions_per_quiz=5, num_quizes=7):   

    q = MultipleChoiceQuestion(
                text="What day is today?",
                options=["Sunday", "Monday", "Tuesday", "Wednesday"],
                answer=0)

    questions = [q for _ in range(num_questions_per_quiz)]
    

    module_tasks = []
    for i in range(num_quizes):
        
        quiz = MultipleChoiceQuiz(
            name="Quiz {}".format(i+1),
            questions=questions)    
        
        module_tasks.append(quiz)

    module = Module(name=name, tasks=module_tasks)
    return module

@main.route("/test")
def render_test():
    module = create_module()
    return render_template("tests/render_module", module=module)