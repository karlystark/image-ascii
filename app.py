from flask import Flask, render_template, request
from flask_cors import CORS
from PIL import Image
import io

app = Flask(__name__)

# activate CORS
CORS(
    app,
    resources={r"/*": {"origins": "*"}},
    allow_headers=["Content-Type"],
    methods=["POST", "GET", "OPTIONS"]
)


###### IMAGE => ASCII FUNCTIONS #########

# 17 chars long from most to least dense
ASCII_CHARS = "@#&%8XKO*o=+:,._  "

# calculates the correct index/char for the density of the given pixel
def pixel_to_ascii(pixel):
    return ASCII_CHARS[pixel // 15]

# converts the image to ascii art
def image_to_ascii(img, new_width=100):
    # resize image to maintain aspect ratio
    width, height = img.size
    aspect_ratio = height / width
    new_height = int(aspect_ratio * new_width * 0.5)
    resized_img = img.resize((new_width, new_height))

    # convert the image to grayscale
    grayscale_img = resized_img.convert('L')

    # generate the ASCII art
    ascii_art = ""

    for y in range(new_height):
        for x in range(new_width):
            # grabs the pixel value at each coordinate
            pixel = grayscale_img.getpixel((x, y))
            # converts pixel value to ascii character
            ascii_art += pixel_to_ascii(pixel)
        # make sure to break to a new line after each row
        ascii_art += "\n"

    return ascii_art


##### ROUTES ######

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert_image():
    if 'image' not in request.files:
        return 'No image found!', 400

    image_file = request.files['image']

    image = Image.open(io.BytesIO(image_file.read()))

    ascii_art = image_to_ascii(image)
    return ascii_art

if __name__ == '__main__':
    app.run(debug=False)