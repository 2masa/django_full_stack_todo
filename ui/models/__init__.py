from enum import StrEnum
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import Length, DataRequired,Optional


# Assuming you have these already from your API model
class TodoStatus(StrEnum):
    OPEN = "Open"
    PENDING = "Pending"
    INPROGRESS = "InProgress"
    CANCELLED = "Cancelled"
    COMPLETED = "Completed"
    

class TodoPriorityStatus(StrEnum):
    HIGHEST = "Highest"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"



def enum_to_choices(enum_cls):
    return [(e.value, e.value) for e in enum_cls]

priority_options = list(TodoPriorityStatus)

status_options = list(TodoStatus)

class CreateTodo(FlaskForm):
    title = StringField("Title",validators=[DataRequired(),Length(min=3)])
    priority = SelectField("Priority",choices=enum_to_choices(TodoPriorityStatus), validators=[DataRequired()])
    status = SelectField("Status",choices=enum_to_choices(TodoStatus), validators=[DataRequired()])
    description = StringField("Description")
    add_button = SubmitField("Add")

class UpdateTodo(FlaskForm):
    title = StringField("Title",validators=[Optional(),Length(min=3)])
    priority = SelectField("Priority",choices=enum_to_choices(TodoPriorityStatus), validators=[Optional()])
    status = SelectField("Status",choices=enum_to_choices(TodoStatus), validators=[Optional()])
    description = StringField("Description",validators=[Optional()])
    add_button = SubmitField("Edit")
