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
    """
    color_mode:
        None = regular grayscale ASCII
        "color" = use pixel RGB color
        "matrix" = green on black
    """
    width, height = img.size
    pxls = img.load()
    
    #if using color modes, convert to RGB
    if color_mode in ("color", "matrix"):
        img = img.convert("RGB")
        pxls = img.load()

    asciiart = []

    for y in range(0, height, blockheight):
        line = ""
        for x in range(0, width, blockwidth):
            blocksum = 0
            count = 0
            r_sum, g_sum, b_sum = 0, 0, 0

            for dy in range(blockheight):
                for dx in range(blockwidth):
                    px = x + dx
                    py = y + dy

                    if px < width and py < height:
                        if color_mode in ("color", "matrix"):
                            r, g, b = pxls[px, py]
                            r_sum += r
                            g_sum += g
                            b_sum += b
                            #use average brightness for mapping
                            brightness = int((r + g + b)/3)
                            blocksum += brightness
                        else:
                            blocksum += pxls[px, py]
                        count += 1

            blockavg = blocksum // count
            char = pixel_to_ascii(blockavg, styleset)

            if color_mode == "color":
                #get average rgb value for the block
                r_avg = r_sum // count
                g_avg = g_sum // count
                b_avg = b_sum // count
                line += f'<span style="color: rgb({r_avg},{g_avg},{b_avg})">{char}</span>'
            elif color_mode == "matrix":
    
                g_val = int(blockavg)
                line += f'<span style="color: rgb(0,{g_val},0)">{char}</span>'
            else:
                line += char

        asciiart.append(line)

    #if using color modes, join with <br>, otherwise create a new line
    if color_mode in ("color", "matrix"):
        return "<br>".join(asciiart)
    else:
        return "\n".join(asciiart)
