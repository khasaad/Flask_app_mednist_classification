import os
import sys

from datetime import datetime

import logging

from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
from inference import get_prediction

app = Flask(__name__)
app.jinja_env.globals.update(zip=zip)

# Create logger
# log = logging.getLogger()

# logging configuration
# logging.basicConfig(filename="log_file.log", level=logging. DEBUG,
#                     format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
#                     datefmt='%d-%m-%y %H:%M:%S')
# logging.debug('This will get logged')

# Script execution
# log.warning("Script Started : " + datetime.today().strftime("%d/%m/%Y %H:%M:%S"))


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'files' not in request.files:
            print("redirection")
            return redirect(request.url)
        # file = request.files.get('file') for one image
        files = request.files.getlist('files')
        # if file.filename == '':
        #     flash('No selected file')
        #     return redirect(request.url)
        list_class_name = []
        list_class_id = []
        list_images = []
        for file in files:
            if not file:
                # continue ## add a message
                return redirect(request.url)  # add this part to avoid an error
            img_bytes = file.read()
            class_name = get_prediction(image_bytes=img_bytes)[0]
            class_id = get_prediction(image_bytes=img_bytes)[1]
            list_class_name.append(class_name)
            list_class_id.append(class_id)
            # ass_name = list(class_name)
            # print('predict', ass_name[0])
            filename = secure_filename(file.filename)
            file.stream.seek(0)
            file.save(os.path.join('static/predicted_images', class_name, filename))
            list_images.append(os.path.join('static/predicted_images', class_name, filename))

        # app.logger.info('Processing default request')
        return render_template('result.html',
                               class_name=list_class_name, class_id=list_class_id,
                               class_image=list_images, zip=zip)

    return render_template('index.html')


if __name__ == '__main__':

    logFormatStr = '[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s'
    logging.basicConfig(format=logFormatStr, filename="global.log", level=logging.DEBUG)
    # Create formatter and add it to the handlers
    formatter = logging.Formatter(logFormatStr, '%d/%m/%Y %H:%M:%S')
    # Create file handler which logs even debug messages
    fileHandler = logging.FileHandler("summary.log")
    fileHandler.setLevel(logging.DEBUG)
    fileHandler.setFormatter(formatter)
    # To write logs to console window in Python.
    # By passing sys.stdout to the logging.StreamHandler() function,
    # we can create a stream handler that can print the log message to the console window.
    streamHandler = logging.StreamHandler(sys.stdout)
    # Set level: Debug
    streamHandler.setLevel(logging.DEBUG)
    streamHandler.setFormatter(formatter)
    # We can then add this stream handler to our logger object with the addHandler() function.
    app.logger.addHandler(fileHandler)
    app.logger.addHandler(streamHandler)
    app.logger.info("Logging is set up.")

    app.run(debug=True, port=int(os.environ.get('PORT', 5000)))


