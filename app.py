import os
import shutil
from plate_detector import plate_finder
from flask import Flask, render_template, request

UPLOAD_FOLDER = '/static/uploads/'
# clean the upload folder
shutil.rmtree(os.getcwd() + UPLOAD_FOLDER)

# clean the upload folder
os.makedirs(os.getcwd() + UPLOAD_FOLDER)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home_page():
    return render_template('index.html')


@app.route('/upload/', methods=['GET', 'POST'])
def upload_page():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return render_template('upload.html', msg='No file selected')
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            return render_template('upload.html', msg='No file selected')

        if file and allowed_file(file.filename):
            file.save(os.path.join(os.getcwd() + UPLOAD_FOLDER, file.filename))
            # call the license plate detection function
            extracted_text = plate_finder(file)
            plate_name = 'plate.png'
            return render_template('upload.html', msg='Successfully processed', extracted_text=extracted_text,
                                   img_src=UPLOAD_FOLDER + file.filename, img_src1=UPLOAD_FOLDER + plate_name)
    elif request.method == 'GET':
        return render_template('upload.html')


if __name__ == '__main__':
    app.run(debug='True')
