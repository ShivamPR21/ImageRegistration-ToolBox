from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import SelectField, SubmitField


class RegisterForm(FlaskForm):
    """
    PCA analysis form
    """
    file_name = FileField(label='File Path:',
                          validators=[FileRequired()]
                          )
    pca_method = SelectField(label='method:',
                             choices=[('std', 'Standardised PCA'),
                                      ('nstd', 'Non-Standardised PCA')]
                             )
    submit = SubmitField(label='Start Analysis')
