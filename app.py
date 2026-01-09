from flask import Flask, render_template, request, send_file
from PIL import Image
from ascii_converter import asciify, styles, prepimage
import io

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    asciiart = None

    if request.method == "POST":
        print("POST RECEIVED")

        #user uploads an image
        file = request.files["image"]
        img = Image.open(file)

        #user chooses a desired width for the ascii art
        desired_width = int(request.form.get("width", 300))
        img = prepimage(img, desired_width)

        #user chooses a style
        selected_style = request.form.get("style", "classic")

        #user selects color mode
        selected_color_mode = request.form.get("color_mode")  # None, "color", "matrix"
        #create block shading parameters based on user selected options
        target_width = int(request.form.get("width", 120))  
        blockwidth = max(1, img.width // target_width)
        blockheight = max(1, int(blockwidth * 0.55))

        #create the ascii art
    asciiart = asciify(
        img,
        styles[selected_style],
        blockwidth=blockwidth,
        blockheight=blockheight,
        color_mode=selected_color_mode
    )



    #Render html template with the art
    return render_template("index.html", asciiart=asciiart, styles=styles)

#Download route to get ascii art as .txt file
@app.route("/download", methods=["POST"])
def download():
   
    ascii_data = request.form["ascii_data"]

    
    return send_file(
        io.BytesIO(ascii_data.encode("utf-8")),
        mimetype="text/plain",
        as_attachment=True,
        download_name="ascii_art.txt"
    )


import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
