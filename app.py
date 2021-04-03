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
    if form.validate_on_submit():
        upload_path = os.path.join('static/uploads/data/', secure_filename(form.file_name.data.filename))
        form.file_name.data.save(upload_path)
        method = form.pca_method.data

        cache_path = 'static/uploads/cache/'
        # Read file from local upload
        # try:
        global img_proc
        if method == 'std':
            img_proc = ImageryProc(upload_path, cache_path)
        elif method == 'nstd':
            img_proc = ImageryProc(upload_path, cache_path, False)

        img_proc.init_pca()
        print("PCA Init")
        img_proc.pca()
        print("PCA computed")
        img_proc.analyse()
        print("Analyse PCA")
        # except:
        #     print("Some Error Occurred")
        img_proc.pca_viz()

        pcs_path = os.listdir('static/uploads/cache/pcs')
        print(pcs_path)

        return render_template('index.html', app_name='PCA App', form=form
                               , shrink="col-2", show_form='', show_result='show',
                               pcs_path=['uploads/cache/pcs/pc_0.png',
                                         'uploads/cache/pcs/pc_1.png',
                                         'uploads/cache/pcs/pc_2.png',
                                         'uploads/cache/pcs/pc_3.png'],
                               covar_path='uploads/cache/covar.png',
                               pcs_covar_path='uploads/cache/pc.png',
                               eig_val=img_proc.eigenval.ravel(),
                               eig_vec=img_proc.eigenvec)

    if form.errors != {}:  # If there are not errors from the validations
        for err_msg in form.errors.values():
            print(f'There was an error with creating a user: {err_msg}')

    return render_template('index.html', app_name='PCA App',
                           form=form, shrink="col-2", pcs_path=['', '', '', ''],
                           covar_path='',
                           pcs_covar_path='',
                           eig_val=[0, 0, 0, 0],
                           eig_vec=[0, 0, 0, 0]
                           )


if __name__ == '__main__':
    app.run(debug=True)
