from random import shuffle
from flask_wtf import FlaskForm
from wtforms import RadioField, FieldList, FormField, SubmitField

from ..models import MultipleChoiceQuestion, QUESTION_TOPICS

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

class MultipleChoiceQuestionForm(FlaskForm):
    answer = RadioField()

    @staticmethod
    def from_mongo_obj(obj, option_tags=ALPHABET):
        form = MultipleChoiceQuestionForm()
        form.answer.choices = [(option_tags[i], obj.options[i]) for i in range(len(obj.options))]
        return form

class MultipleChoiceQuizForm(FlaskForm):
    questions = FieldList(FormField(MultipleChoiceQuestionForm))

    submit = SubmitField("Entregar evaluación")

    @staticmethod
    def from_mongo_obj(questions):
        form = MultipleChoiceQuizForm()
        for q in questions:
            form.questions.append_entry(MultipleChoiceQuestionForm.from_mongo_obj(q))

        return form
    
    @staticmethod
    def generate_random_quiz(topic, num_questions):

        # Validate the topic.        
        if topic not in QUESTION_TOPICS:
            raise ValueError("Invalid quiz topic.")

        
        questions = MultipleChoiceQuestion.objects(topic=topic)

        if len(questions) < num_questions:
            raise ValueError("Not enough questions of that topic were found.")
        
        shuffle(questions)
        questions = questions.slice([0, num_questions])
