import random 
from flask_wtf import FlaskForm
from wtforms import RadioField, FieldList, FormField, SubmitField

from ..models import MultipleChoiceQuestion, QUESTION_TOPICS

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
DEFAULT_CHOICES = ["Option 1", "Option 2","Option 3", "Option 4"]

class MultipleChoiceQuestionForm(FlaskForm):
    class Meta:
        csrf_token = False

    answer = RadioField(label='')

    # The default parameters are placeholder values to make possible mock construction
    # during instantiation of MultipleChoiceQuizForm.
    def __init__(self, question_text="[PLACEHOLDER_TEXT]", choices=DEFAULT_CHOICES, 
                correct_answer=0, choice_tags=ALPHABET, **kwargs):
        super().__init__(**kwargs)
        self.initialize(question_text=question_text, 
                        choices=choices, 
                        correct_answer=correct_answer,
                        choice_tags=choice_tags)

    def initialize(self, question_text, choices, correct_answer, choice_tags):
        self.answer.choices = [(choice_tags[i], choices[i]) for i in range(len(choices))]
        self.text = question_text
        self.correct_answer = choice_tags[correct_answer]

    def is_correct(self):
        return self.answer.data == self.correct_answer

    @staticmethod
    def from_mongo_obj(obj, **kwargs):
        return MultipleChoiceQuestionForm(
            question_text=obj.text,
            choices=obj.choices,
            correct_answer=obj.answer, 
            **kwargs)

class MultipleChoiceQuizForm(FlaskForm):
    class Meta:
        csrf_token = False
        
    questions = FieldList(FormField(MultipleChoiceQuestionForm))
    
    submit = SubmitField("Entregar evaluación")

    def get_score(self):
        return  sum([question.is_correct() for question in self.questions])

    def get_max_score(self):
        return len(self.questions)

    @staticmethod
    def from_mongo_obj(questions_mongo):
        form = MultipleChoiceQuizForm()
        for question_mongo in questions_mongo:
            form.questions.append_entry(
                MultipleChoiceQuestionForm.from_mongo_obj(question_mongo))
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
        return MultipleChoiceQuizForm.from_mongo_obj(questions)
        #return MultipleChoiceQuizForm()