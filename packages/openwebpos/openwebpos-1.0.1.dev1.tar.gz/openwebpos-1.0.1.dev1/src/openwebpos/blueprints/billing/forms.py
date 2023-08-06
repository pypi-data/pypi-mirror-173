from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField
from wtforms.validators import DataRequired, NumberRange


class PaymentAmountForm(FlaskForm):
    amount = IntegerField('Amount',
                          validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Submit')
