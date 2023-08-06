from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, \
    FloatField
from wtforms.validators import DataRequired, Length, NumberRange

from openwebpos.blueprints.pos.models import MenuType, MenuCategory, Ingredient


class MenuTypeForm(FlaskForm):
    short_name = StringField('Short Name',
                             validators=[DataRequired(), Length(min=2, max=20)])
    name = StringField('Name',
                       validators=[DataRequired(), Length(min=2, max=100)])
    description = StringField('Description',
                              validators=[DataRequired(),
                                          Length(min=2, max=255)])
    submit = SubmitField('Submit')


class MenuCategoryForm(FlaskForm):
    menu_type_id = SelectField('Menu Type', coerce=int)
    short_name = StringField('Short Name',
                             validators=[DataRequired(), Length(min=2, max=20)])
    name = StringField('Name',
                       validators=[DataRequired(), Length(min=2, max=100)])
    description = StringField('Description',
                              validators=[DataRequired(),
                                          Length(min=2, max=255)])
    submit = SubmitField('Submit')

    def set_choices(self):
        self.menu_type_id.choices = [(menu_type.id, menu_type.name)
                                     for menu_type in MenuType.query.all()]

    # def __init__(self):
    #     super(MenuCategoryForm, self).__init__()
    #     self.menu_type_id.choices = [(menu_type.id, menu_type.name)
    #                                  for menu_type in MenuType.query.all()]


class MenuItemForm(FlaskForm):
    menu_category_id = SelectField('Menu Category', coerce=int)
    short_name = StringField('Short Name',
                             validators=[DataRequired(), Length(min=2, max=20)])
    name = StringField('Name',
                       validators=[DataRequired(), Length(min=2, max=100)])
    description = StringField('Description',
                              validators=[DataRequired(),
                                          Length(min=2, max=255)])
    price = FloatField('Price', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Submit')

    def set_choices(self):
        self.menu_category_id.choices = [(menu_category.id, menu_category.name)
                                         for menu_category in
                                         MenuCategory.query.all()]


class QuantityForm(FlaskForm):
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    submit = SubmitField('Submit')


class IngredientForm(FlaskForm):
    name = StringField('Name',
                       validators=[DataRequired(), Length(min=2, max=100)])
    unit = StringField('Unit',
                       validators=[DataRequired(), Length(min=2, max=20)])
    price = FloatField('Price', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Submit')


class MenuItemIngredientForm(FlaskForm):
    ingredient_id = SelectField('Ingredient', coerce=int)
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def set_choices(self):
        self.ingredient_id.choices = [(ingredient.id, ingredient.name)
                                      for ingredient in
                                      Ingredient.query.all()]
