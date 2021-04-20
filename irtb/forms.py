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


class RGBForm(FlaskForm):
    """
    RGB band PCA visualization
    """
    r = SelectField(label='red band:',
                    choices=[('pc_0.png', 'Principal Component 1'),
                             ('pc_1.png', 'Principal Component 2'),
                             ('pc_2.png', 'Principal Component 3'),
                             ('pc_3.png', 'Principal Component 4')]
                    )
    g = SelectField(label='green band:',
                    choices=[('pc_0.png', 'Principal Component 1'),
                             ('pc_1.png', 'Principal Component 2'),
                             ('pc_2.png', 'Principal Component 3'),
                             ('pc_3.png', 'Principal Component 4')]
                    )
    b = SelectField(label='blue band:',
                    choices=[('pc_0.png', 'Principal Component 1'),
                             ('pc_1.png', 'Principal Component 2'),
                             ('pc_2.png', 'Principal Component 3'),
                             ('pc_3.png', 'Principal Component 4')]
                    )
    submit = SubmitField(label='Show Combination')
