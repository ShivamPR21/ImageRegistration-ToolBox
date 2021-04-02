from flask import Flask, render_template

from irtb.forms import RegisterForm

UPLOAD_FOLDER = '/uploads/data'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif', 'L-3'}

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ec9439cfc6c796ae2029594d'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    """
    Check for allowed extensions
    :param filename:
    :return:
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def home_page():
    """
    PCA App Route callback work in "GET" mode
    :return: render_template()
    """
    form = RegisterForm()
    return render_template('index.html', app_name='PCA App', form=form, shrink="col-2")


@app.route('/pca', methods=['POST'])
def form_handle():
    """

    :return:
    """
    form = RegisterForm()
    if form.validate_on_submit():
        file_path = form.file_name.data
        method = form.pca_method.data
        print("Method: ", method,
              "\nFilePath: ", file_path)
        return render_template('index.html', app_name='PCA App', form=form, shrink="col-2", show="show",
                               content=[method, file_path])
    if form.errors != {}:  # If there are not errors from the validations
        for err_msg in form.errors.values():
            print(f'There was an error with creating a user: {err_msg}')


# @app.route('/tmp')
# def tmp_page():
#     return render_template('tmp.html')

if __name__ == '__main__':
    app.run(debug=True)
