from flask_wtf import FlaskForm
from wtforms import SelectField, FileField, SubmitField


class RegisterForm(FlaskForm):
    """
    PCA analysis form
    """
    file_name = FileField(label='File Path:')
    pca_method = SelectField(label='method:', choices=[('method1', 'method1'), ('method2', 'method2')])
    submit = SubmitField(label='Start Analysis')
