from flask_wtf import FlaskForm
from wtforms import RadioField, FieldList, FormField, SubmitField

from ..models import MultipleChoiceQuiz, MultipleChoiceQuestion

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

    submit = SubmitField("Entregar examen")

    @staticmethod
    def from_mongo_obj(obj):
        form = MultipleChoiceQuizForm()
        for q in obj.questions:
            form.questions.append_entry(MultipleChoiceQuestionForm.from_mongo_obj(q))

        return form