import os

from flask import Flask, render_template
from werkzeug.utils import secure_filename

from irtb.forms import TransForm
from irtb.transform import TransformProc

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
    form = TransForm()
    data_dir = 'static/uploads/data/'
    cache_dir = 'static/uploads/cache/'

    if form.validate_on_submit():
        upload_path = os.path.join(data_dir, secure_filename(form.file_name.data.filename))
        print('upload path ', upload_path)
        form.file_name.data.save(upload_path)
        form_data = {'t_x': form.translation_x.data,
                     't_y': form.translation_y.data,
                     'rot': form.rotation.data,
                     'scale_x': form.scale_x.data,
                     'scale_y': form.scale_y.data,
                     'skew_x': form.skew_x.data,
                     'skew_y': form.skew_y.data,
                     'interp_method': form.interpolation_method.data}

        transform = TransformProc(upload_path, cache_dir, form_data)
        res = transform.transform()

        return render_template('results.html', app_name='Affine App', results=res)

    if form.errors != {}:  # If there are not errors from the validations
        for err_msg in form.errors.values():
            print(f'There was an error with creating a user: {err_msg}')

    return render_template('index.html', app_name='Affine App', form=form)

@app.route('/results', methods=['GET'])
def results():
    return render_template('results.html', app_name='Affine App')

if __name__ == '__main__':
    app.run(debug=True)
