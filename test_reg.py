import unittest
import werkzeug
from werkzeug.datastructures import FileStorage

from app import *
from inference import *
from commons import *

BASE_DIR = 'C:/Users/khale/Downloads/mednist-classification-master noura/mednist-classification-master/'


class FlaskTestCase(unittest.TestCase):

    def test_app(self):
        # test server loads correctly
        response = app.test_client(self)
        response = response.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_get_single_prediction(self):
        # test with a valid image
        image_path = f'{BASE_DIR}/static/predicted_images/ChestCT/000001.jpeg'

        # im = Image.open(image_path)
        # imgByteArr = io.BytesIO()
        # im.save(imgByteArr, format=im.format)
        # image = imgByteArr.getvalue()
        file_loc = open(image_path, 'rb')
        file = werkzeug.datastructures.FileStorage(file_loc)
        image = file.read()
        class_name = get_prediction(image_bytes=image)[0]
        class_id = get_prediction(image_bytes=image)[1]
        self.assertEqual((class_name, class_id), ('ChestCT', 2))

    def test_get_predictions(self):
        # test with a lists of valid images
        df = {'filename': [], 'class_name': [], 'class_id': []}
        for file in os.listdir(f'{BASE_DIR}/static/predicted_images/ChestCT/'):
            image_path = f'{BASE_DIR}/static/predicted_images/ChestCT/{file}'
            file_loc = open(image_path, 'rb')
            file = werkzeug.datastructures.FileStorage(file_loc)
            image = file.read()
            class_name = get_prediction(image_bytes=image)[0]
            class_id = get_prediction(image_bytes=image)[1]
            df['filename'].append(file)
            df['class_name'].append(class_name)
            df['class_id'].append(class_id)

        self.assertEqual((df['class_name'][2], df['class_id'][2]), ('ChestCT', 2))


if __name__ == '__main__':
    unittest.main()