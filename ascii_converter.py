from PIL import Image

# All the available styles for user to select
styles = {
    "classic": " .:-=+*#%@",
    "blocks": " ░▒▓█",
    "detailed": " .'`^\",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$",
    "dots": " .`'",
    "shades": " ░░▒▒▓▓█",
    "symbols": "@#$%&*+=-:. ",
    "matrix": "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%^&*",
    "weirdblocks": "▁▂▃▄▅▆▇█"
}

#prepare image by resizing and converting to grayscale if needed
def prepimage(img, desired_width):
    # grayscale
    img = img.convert("L")
    # resize
    original_width, original_height = img.size
    aspect_ratio = original_height / original_width
    desired_height = int(aspect_ratio * desired_width * 0.55)
    img = img.resize((desired_width, desired_height))
    return img

#brightness mapping to ascii characters
def pixel_to_ascii(pixelval, styleset, invert=True):
    if invert:
        pixelval = 255 - pixelval
    index = pixelval * (len(styleset) - 1) // 255
    return styleset[index]

def asciify(img, styleset, blockwidth, blockheight, color_mode=None):
    width, height = img.size 
    pxls = img.load()

    asciiart = []

    for y in range(0, height, blockheight):
        line = ""

        for x in range(0, width, blockwidth):
            r_sum = g_sum = b_sum = 0
            blocksum = 0
            count = 0

            for dy in range(blockheight):
                for dx in range(blockwidth):
                    px = x + dx
                    py = y + dy

                    if px < width and py < height:
                        if color_mode == "color" or color_mode == "matrix":
                            r, g, b = pxls[px, py][:3]
                            r_sum += r
                            g_sum += g
                            b_sum += b
                        else:  #grayscale
                            blocksum += pxls[px, py]
                        count += 1

            if count == 0:
                continue

            if color_mode == "color":
                #average color values
                r_avg = r_sum // count
                g_avg = g_sum // count
                b_avg = b_sum // count
                #when using color mode, use a solid block
                line += f'<span style="color: rgb({r_avg},{g_avg},{b_avg})">█</span>'

            elif color_mode == "matrix":
                #green average for matrix
                g_avg = g_sum // count
                #map green to characters
                index = g_avg * (len(styleset) - 1) // 255
                line += f'<span style="color: rgb(0,{g_avg},0)">{styleset[index]}</span>'

            else:
                #regular grayscale ascii
                blockavg = blocksum // count
                line += pixel_to_ascii(blockavg, styleset)

        asciiart.append(line)

    return "\n".join(asciiart)
