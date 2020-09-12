import random 
from flask_wtf import FlaskForm
from wtforms import RadioField, FieldList, FormField, SubmitField

from ..models import MultipleChoiceQuestion, QUESTION_TOPICS

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

class MultipleChoiceQuestionForm(FlaskForm):
    answer = RadioField()

    def __init__(self, question_text, choices, correct_answer, choice_tags=ALPHABET):
        super().__init__()
        self.answer.choices = [(choice_tags[i], choices[i]) for i in range(len(choices))]
        self.text = question_text
        self.correct_answer = choice_tags[correct_answer]

    def is_correct(self):
        return self.answer.data == self.correct_answer

    @staticmethod
    def from_mongo_obj(obj):
        return MultipleChoiceQuestionForm(
            question_text=obj.text,
            choices=obj.choices,
            correct_answer=obj.answer)

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
        """
        Generates a multiple choice quiz from a given topic and number of questions.
        Fetches random questions from the question bank in the database.
        """

        # Validate the topic.        
        if topic not in QUESTION_TOPICS:
            raise ValueError("Invalid quiz topic.")

        # Get all questions that match in topic
        questions = MultipleChoiceQuestion.objects(topic=topic)

        # Validate that there are enough questions.
        if len(questions) < num_questions:
            raise ValueError("Not enough questions of that topic were found.")
        
        # Choose the questions randomly.
        questions = random.choices(questions, k=num_questions)
        
        # Convert the question from mongoengine model objects to wtforms.
        questions = [MultipleChoiceQuestionForm.from_mongo_obj(question_mongo) for question_mongo in questions]

        MultipleChoiceQuestionForm

