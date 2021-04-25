import os

import cv2
import numpy as np
from flask import Flask, render_template
from werkzeug.utils import secure_filename

from irtb.forms import IRTBform
from irtb.forms import LoadImageForm
from irtb.registration import align_images

UPLOAD_FOLDER = '/uploads/data'
# ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif', 'L-3'}

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ec9439cfc6c796ae2029594d'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

src_path = None
tgt_path = None


@app.route('/', methods=['GET', 'POST'])
def home_page():
    """
    PCA App Route callback work in "GET" mode
    :return: render_template()
    """
    form = LoadImageForm()
    ir_form = IRTBform()
    global src_path, tgt_path

    if form.validate_on_submit():
        src_path = os.path.join('uploads/data/', secure_filename(form.source_fn.data.filename))
        form.source_fn.data.save(os.path.join('static', src_path))
        tgt_path = os.path.join('uploads/data/', secure_filename(form.target_fn.data.filename))
        form.target_fn.data.save(os.path.join('static', tgt_path))

        return render_template('irtb.html', src_path=src_path, tgt_path=tgt_path,
                               randoms=np.random.randint(100000000, size=2), form=ir_form)
    if form.errors != {}:  # If there are not errors from the validations
        for err_msg in form.errors.values():
            print(f'There was an error with creating a user: {err_msg}')

    if ir_form.validate_on_submit():
        # global src_path, tgt_path
        image = cv2.imread(os.path.join('static', src_path))
        template = cv2.imread(os.path.join('static', tgt_path))

        if ir_form.method.data == 'feature':
            feature = ir_form.feature.data
            keepPercentage = ir_form.kpp.data
            if ir_form.matchingMetric.data == 'Hamming':
                aligned = align_images(image, template,
                                       matching_method=cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING,
                                       feature_method=feature, keepPercent=keepPercentage)
            elif ir_form.matchingMetric.data == 'HammingLUT':
                aligned = align_images(image, template,
                                       matching_method=cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMINGLUT,
                                       feature_method=feature, keepPercent=keepPercentage)
            elif ir_form.matchingMetric.data == 'L1':
                aligned = align_images(image, template,
                                       matching_method=cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_L1,
                                       feature_method=feature, keepPercent=keepPercentage)
            elif ir_form.matchingMetric.data == 'L2':
                aligned = align_images(image, template,
                                       matching_method=cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_SL2,
                                       feature_method=feature, keepPercent=keepPercentage)
        return render_template('irtb_results.html',
                               feature_img='/uploads/cache/feature.png',
                               tgt_img=tgt_path, src_img=src_path, alg_img='/uploads/cache/final.png',
                               randoms=np.random.randint(100000000,
                                                         size=4))

    if ir_form.errors != {}:  # If there are not errors from the validations
        for err_msg in ir_form.errors.values():
            print(f'There was an error with creating a user: {err_msg}')
    return render_template('index.html', app_name='IRTB App',
                           form=form)


if __name__ == '__main__':
    app.run(debug=True)
