from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import SelectField, FloatField, SubmitField


class RegisterForm(FlaskForm):
    """
    PCA analysis form
    """
    file_name = FileField(label='File Path:',
                          validators=[FileRequired()]
                          )
    translation_x = FloatField(label='Translation X:',
                               validators=[FileRequired()]
                               )
    translation_y = FloatField(label='Translation Y:',
                               validators=[FileRequired()]
                               )
    rotation = FloatField(label='Rotation:',
                          validators=[FileRequired()]
                          )
    scale_x = FloatField(label='Scale X:',
                         validators=[FileRequired()]
                         )
    scale_y = FloatField(label='Scale Y:',
                         validators=[FileRequired()]
                         )
    skew_x = FloatField(label='Skew X:',
                        validators=[FileRequired()]
                        )
    skew_y = FloatField(label='Skew Y:',
                        validators=[FileRequired()]
                        )
    interpolation_method = SelectField(label='Interpolation Method:',
                                       choices=[('nn', 'Nearest Neighbour'),
                                                ('bi-linear', 'Bi-Linear'),
                                                ('bi-cubic', 'Bi-Cubic')]
                                       )

    submit = SubmitField(label='Warp Image')
