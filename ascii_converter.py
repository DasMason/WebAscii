from PIL import Image

#All the available styles for user to select
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

#prepare uploaded image to be converted to ascii
def prepimage(img, desired_width):
    #grayscale
    img = img.convert("L")

    #resize
    original_width, original_height = img.size
    aspect_ratio = original_height / original_width

    desired_height = int(aspect_ratio * desired_width * 0.55)

    img = img.resize((desired_width, desired_height))

    return img

#determine brightness of block cells and map to ascii characters
def pixel_to_ascii(pixelval, styleset, invert=True):
    if invert:
        pixelval = 255 - pixelval
    index = pixelval * (len(styleset) - 1) // 255
    return styleset[index]

#convert the block cells of the image to characters
def asciify(img, styleset, blockwidth, blockheight):
    width, height = img.size 
    pxls = img.load()

    asciiart = []

    for y in range(0, height, blockheight):
        line = ""

        for x in range(0, width, blockwidth):
            blocksum = 0
            count = 0

            for dy in range(blockheight):
                for dx in range(blockwidth):
                    px = x + dx
                    py = y + dy

                    if px < width and py < height:
                        blocksum += pxls[px, py]
                        count += 1

            blockavg = blocksum // count
            line += pixel_to_ascii(blockavg, styleset)

        asciiart.append(line)

    return "\n".join(asciiart)

