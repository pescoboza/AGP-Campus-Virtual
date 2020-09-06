
#########################################################################
# Test for module model
#########################################################################
from app.models import MultipleChoiceQuestion, MultipleChoiceQuiz, Module

def test_module():
    NUM_QUESTIONS_PER_QUIZ = 5
    NUM_QUIZES = 3

    q = MultipleChoiceQuestion(
                text="What day is today?",
                options=["Sunday", "Monday", "Tuesday", "Wednesday"],
                answer=0)

    questions = [q for _ in range(NUM_QUESTIONS_PER_QUIZ)]
    

    module_tasks = []
    for i in range(NUM_QUIZES):
        
        quiz = MultipleChoiceQuiz(
            name="Quiz {}".format(i+1),
            questions=questions)    
        
        module_tasks.append(quiz)

    module = Module(name="Test Module", tasks=module_tasks)
    module.save()
    # with open("module_test.json", 'w') as outfile:
    #     outfile.write(module.to_json())