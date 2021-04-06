import os

from flask import Flask, render_template
from werkzeug.utils import secure_filename

from irtb.forms import RegisterForm
from irtb.io import ImageryProc

UPLOAD_FOLDER = '/uploads/data'
# ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif', 'L-3'}

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ec9439cfc6c796ae2029594d'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

img_proc = None


@app.route('/', methods=['GET', 'POST'])
def home_page():
    """
    PCA App Route callback work in "GET" mode
    :return: render_template()
    """
    form = RegisterForm()

    return render_template('index.html', app_name='Affine App', form=form)


if __name__ == '__main__':
    app.run(debug=True)
