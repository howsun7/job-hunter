import warnings
from sqlalchemy.sql.base import  ImmutableColumnCollection
from sqlalchemy import types
from sqlalchemy_utils import types as utils_types
from flask_sqlalchemy import model as alchemy_model

from models import Company, Skill, Job
from exceptions import EmptyCollectionError, EmptyFieldsError


class Question:
    """
    make question based on field type
    
    ask question and validate answer based on field type (Integer...)

    examples:
    - str
        Question: What is the {company (table.name)} {name (field.name)}?
        Question: What is the {sklll (table.name)} {name (field.name)}?

    - int
        Question: what is the {yoe (field.name)} for the {job (table.name)}?

    - url
        Question: what is the {job (table.name)} {link (field.name)}
    """

    def __init__(self, column_field):
        self.field_name = column_field.name
        self.table_name = column_field.table.name
        self.field_type = column_field.type
        # self.question_text = None
        self.answer = None


class QuestionCollection:
    """    
    a collection of model columns field that should be turn into questions

    - all columns 
    - all relevant fields
    - all questions
    """

    question_cls = Question
    included_models = [Company, Skill, Job]
    excluded_fieldnames = ['created_at', 'updated_at']
    
    # attribute: callback -> condition
    # filter out field for {attribute} when callback is evaulated as True
    attr_to_filter_out = {
        'primary_key': lambda arg: arg == True,
        'foreign_keys': lambda arg: len(arg) > 0,
        'name': lambda arg: arg in QuestionCollection.excluded_fieldnames
    }

    all_columns = []
    
    def __init__(self):
        self.fields = []
        self.questions = []
        QuestionCollection.load_all_table_columns()

    @classmethod
    def load_all_table_columns(cls):
        for model in cls.included_models:
            model_columns = cls.get_table_columns(model)
            cls.all_columns.extend(model_columns)
        
        if not cls.all_columns:
            warnings.warn('Empty collection after an attempt to load all table columns')
    
    @staticmethod
    def get_table_columns(model: alchemy_model.DefaultMeta) -> ImmutableColumnCollection:
        """return all table columns of a model"""        
        return model.__table__.columns    

    def get_relevant_fields(self):
        if not self.all_columns:
            raise EmptyCollectionError

        for column in self.all_columns:
            to_add = True
            for attribute, callback in self.attr_to_filter_out.items():            
                field_attribute = vars(column).get(attribute)

                # filter when any of field_attribute callback evaulates to True
                if field_attribute and callback(field_attribute):
                    to_add = False
                    break
            
            if to_add:
                self.fields.append(column)

    def make_questions(self):
        if not self.fields:
            raise EmptyFieldsError

        for field in self.fields:
            question = self.question_cls(field)
            self.questions.append(question)
            
    
if __name__ == '__main__':
    qc = QuestionCollection()
    qc.get_relevant_fields()

    