import os

import numpy as np
from flask import Flask, render_template
from werkzeug.utils import secure_filename

from irtb.forms import TransForm

import cv2

from copy import copy

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
        form.file_name.data.save(upload_path)
        img = cv2.imread(upload_path, cv2.IMREAD_COLOR)

        if form.str_method.data == 'linear':
            norm_img = cv2.normalize(img, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
            norm_img = (255 * norm_img).astype(np.uint8)
            cv2.imwrite(os.path.join(cache_dir, 'final.png'), norm_img)
        elif form.str_method.data == 'hist':
            norm_img = copy(img)
            for i in range(np.shape(img)[2]):
                hist, bins = np.histogram(img[:, :, i].flatten(), 256, [0, 256])

                cdf = hist.cumsum()

                cdf_m = np.ma.masked_equal(cdf, 0)
                cdf_m = (cdf_m - cdf_m.min()) * 255 / (cdf_m.max() - cdf_m.min())
                cdf = np.ma.filled(cdf_m, 0).astype('uint8')

                img2 = cdf[img[:, :, i]]
                norm_img[:, :, i] = img2
            norm_img = norm_img.astype(np.uint8)
            cv2.imwrite(os.path.join(cache_dir, 'final.png'), norm_img)
        elif form.str_method.data == 'gauss':
            norm_img = copy(img)
            for i in range(np.shape(img)[2]):
                sigma = np.std(img[:, :, i])
                mean = np.mean(img[:, :, i])
                norm_img[:, :, i] = (255 / sigma) * (img[:, :, i] - mean)

            norm_img = norm_img.astype(np.uint8)
            cv2.imwrite(os.path.join(cache_dir, 'final.png'), norm_img)

        return render_template('index.html', app_name='Stretching App', form=form,
                               original_img=os.path.join('uploads/data/', str(form.file_name.data.filename)),
                               final_img=os.path.join('uploads/cache/', 'final.png'),
                               randoms=np.random.randint(100000000, size=10))

    if form.errors != {}:  # If there are not errors from the validations
        for err_msg in form.errors.values():
            print(f'There was an error with creating a user: {err_msg}')

    return render_template('index.html', app_name='Stretching App', form=form,
                           randoms=np.random.randint(100000000, size=10))


if __name__ == '__main__':
    app.run(debug=True)
