import warnings
from sqlalchemy.sql.base import  ImmutableColumnCollection
from sqlalchemy import types
from sqlalchemy_utils import types as utils_types
from flask_sqlalchemy import model as alchemy_model
from models import Company, Skill, Job
from exceptions import (
    EmptyCollectionError, EmptyFieldsError, HandlerTypeNotFoundError, QAHandlerDoesNotExistError,
)


class BaseTypeHandler:
    def __init__(self, question):
        self.question = question
        self.constructed_question = None
        self.user_answer = None
        
    def ask_question(self):
        while True:
            if self.constructed_question is None or self.user_answer is None:
                constructed_question = self.make_question()
                user_answer = input(constructed_question)
                user_answer = self.clean_answer(user_answer)
                if self.validate_answer(user_answer):
                    self.user_answer = user_answer
                    break 
                
    def make_question(self):        
        self.constructed_question = "What is the {} {}? ".format(self.question.table_name, self.question.field_name)        
        return self.constructed_question
    
    def clean_answer(self, user_answer):
        return user_answer.strip()

    def validate_answer(self, user_answer):
        """Return True if the user answer is a valid"""
        return True if user_answer != '' else False

class URLTypeHandler(BaseTypeHandler):
    def validate_answer(self, user_answer):
        """return True if user answer is a valid URL"""
        # an example for now (TODO: validate URL)
        return super().validate_answer(user_answer)
        

# types: range, int, string, boolean
QA_TYPE_HANDLERS = {
    types.String: BaseTypeHandler,
    types.Integer: BaseTypeHandler,
    utils_types.url.URLType: URLTypeHandler,
}    

class Question:
    """
    make question based on field type
    
    ask question and validate answer based on field type (Integer...)

    examples:
    {model (table or field)} 
    [missing]

    - str
        Question: What is the {company (table.name)} {name (field.name)}?
        
        # TODO: this is NG...(not handling comma separated values)
        Question: What is the {sklll (table.name)} {name (field.name)}?

    - int
        Question: what is the {yoe (field.name)} [required] for the {job (table.name)}?

    - url
        Question: what is the {job (table.name)} {link (field.name)}
    """

    def __init__(self, column_field):
        self.field_name = column_field.name
        self.table_name = column_field.table.name
        self.field_type = column_field.type
        self.qa_handler = None
        self.load_qa_handler()

    def get_handler_type(self):
        for field_type, type_handler in QA_TYPE_HANDLERS.items():
            if isinstance(self.field_type, field_type):
                return QA_TYPE_HANDLERS[field_type]

        raise HandlerTypeNotFoundError
        
    def load_qa_handler(self):
        handler_type = self.get_handler_type()
        self.qa_handler = handler_type(self)

    def start_qa(self):
        if self.qa_handler is None:
            raise QAHandlerDoesNotExistError

        self.qa_handler.ask_question()
        
    @property
    def answer(self):
        if self.qa_handler is None:
            raise QAHandlerDoesNotExistError
        return self.qa_handler.user_answer
        

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

    def make_questions(self, start_qa=False):
        if not self.fields:
            raise EmptyFieldsError

        # re-make questions if questions already exist
        if self.questions:
            self.questions = [] 
        
        for field in self.fields:
            question = self.question_cls(field)
            if start_qa:
                question.start_qa()
            self.questions.append(question)
            
    
if __name__ == '__main__':
    qc = QuestionCollection()
    qc.get_relevant_fields()
    qc.make_questions(start_qa=False)
    

    