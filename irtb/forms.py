from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import SelectField, SubmitField, IntegerField, FloatField


class LoadImageForm(FlaskForm):
    """
    PCA analysis form
    """
    source_fn = FileField(label='Source Image:',
                          validators=[FileRequired()]
                          )
    target_fn = FileField(label='Target Image:',
                          validators=[FileRequired()]
                          )
    submit = SubmitField(label='Load Images')


class IRTBform(FlaskForm):
    """
    RGB band PCA visualization
    """
    method = SelectField(label='Method:',
                         choices=[('manual', 'Manual'),
                                  ('feature', 'Feature Based'),
                                  ('area', 'Area Based'),
                                  ('NN', 'Conv Neural Networks')]
                         )

    feature = SelectField(label='Feature Extraction Method:',
                          choices=[('sift', 'Scale-Invariant Feature Transform'),
                                   ('surf', 'Speeded-Up Robust Features'),
                                   ('brief', 'Binary Robust Independent Elementary Features'),
                                   ('orb', 'Oriented FAST and Rotated BRIEF')]
                          )

    registrationModel = SelectField(label='Registration model:',
                                    choices=[('homo', 'Homography'),
                                             ('trans', 'Translation'),
                                             ('rot', 'Rotation'),
                                             ('euc', 'Euclidean')]
                                    )

    matchingMetric = SelectField(label='Matching Norm:',
                                 choices=[('L1', 'L1 norm'),
                                          ('L2', 'L2 norm'),
                                          ('Hamming', 'Hamming'),
                                          ('HammingLUT', 'LUT based Hamming')]
                                 )

    maxFeaturePts = IntegerField(label='Maximum feature points:',
                                 default=40)

    kpp = FloatField(label='Fraction of Matches to use:',
                                 default=0.2)

    submit = SubmitField(label='Register Images')
