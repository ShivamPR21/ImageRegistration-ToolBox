import os

import numpy as np
from flask import Flask, render_template, redirect
from werkzeug.utils import secure_filename

from irtb.forms import RegisterForm
from irtb.forms import RGBForm
from irtb.io import ImageryProc

from matplotlib import pyplot as plt

from PIL import Image
import numpy as np

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

@app.route('/rgb', methods=['GET', 'POST'])
def rgb_viz():
    form_rgb = RGBForm()
    if form_rgb.validate_on_submit():
        pc_path = 'static/uploads/cache/pcs'
        r_band = np.asarray(Image.open(os.path.join(pc_path, form_rgb.r.data)).convert("L"))
        g_band = np.asarray(Image.open(os.path.join(pc_path, form_rgb.g.data)).convert("L"))
        b_band = np.asarray(Image.open(os.path.join(pc_path, form_rgb.b.data)).convert("L"))
        # r_band = plt.imread(os.path.join(pc_path, form_rgb.r.data))
        # g_band = plt.imread(os.path.join(pc_path, form_rgb.g.data))
        # b_band = plt.imread(os.path.join(pc_path, form_rgb.b.data))

        print(r_band.shape, form_rgb.r.data)
        print(g_band.shape, form_rgb.g.data)
        print(b_band.shape, form_rgb.b.data)

        final_img = np.zeros([r_band.shape[0], r_band.shape[1], 3])
        final_img[:, :, 0] = r_band/np.max(r_band)
        final_img[:, :, 1] = g_band/np.max(g_band)
        final_img[:, :, 2] = b_band/np.max(b_band)

        # os.remove('static/uploads/cache/pcs/rgb.png')
        plt.imsave('static/uploads/cache/pcs/rgb.png', final_img)
        print(np.random.randint(100000000, size=1)[0])
        # final_path = str('uploads/cache/pcs/rgb.png' + str(np.random.randint(100000000, size=1)[0]))
        tmp = render_template('rgb.html', app_name='PCA App', form=form_rgb,
                              rgb_path=['uploads/cache/pcs/rgb.png', np.random.randint(100000000, size=1)[0]])
        return tmp
        # return render_template('rgb.html', app_name='PCA App', form=form_rgb, rgb_path='assets/demo.jpg')

    return render_template('rgb.html', app_name='PCA App', form=form_rgb, rgb_path='assets/demo.jpg')

if __name__ == '__main__':
    app.run(debug=True)
