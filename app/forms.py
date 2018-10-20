from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, AnyOf

# class LoginForm(FlaskForm):
#     username = StringField('Username', validators=[DataRequired()])
#     password = PasswordField('Password', validators=[DataRequired()])
#     remember_me = BooleanField('Remember Me')
#     submit = SubmitField('Sign In')

class CubeForm(FlaskForm):
    colour = StringField(
        'First letter of colour (choose from b; g; r; y; w; o)',
        [Length(max=1), DataRequired(), AnyOf(['b', 'g', 'r', 'o', 'w', 'y'])]
    )
    submit = SubmitField('Fill in')