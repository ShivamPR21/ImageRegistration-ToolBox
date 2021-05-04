from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import SelectField, FloatField, SubmitField


class TransForm(FlaskForm):
    """
    PCA analysis form
    """
    file_name = FileField(label='File Path:',
                          validators=[FileRequired()]
                          )
    str_method = SelectField(label='Stretch Method:',
                             choices=[('linear', 'Linear Stretch'),
                                      ('hist', 'Histogram Equalization'),
                                      ('gauss', 'Gaussian Stretch')]
                             )

    submit = SubmitField(label='Stretch Contrast')
