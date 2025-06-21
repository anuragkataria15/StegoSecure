from PIL import Image

def text_to_bin(text):
    return ''.join(format(ord(c), '08b') for c in text)

def bin_to_text(binary):
    chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
    return ''.join(chr(int(char, 2)) for char in chars)

def hide_data(img_path, message, out_path="output.png"):
    img = Image.open(img_path)
    binary = text_to_bin(message) + '1111111111111110'  # EOF marker
    data = iter(binary)
    pixels = list(img.getdata())

    for i in range(len(pixels)):
        r, g, b = pixels[i]
        try:
            r = (r & ~1) | int(next(data))
            g = (g & ~1) | int(next(data))
            b = (b & ~1) | int(next(data))
        except StopIteration:
            pixels[i] = (r, g, b)
            break
        pixels[i] = (r, g, b)

    img.putdata(pixels)
    img.save(out_path)
    return out_path

def extract_data(img_path):
    img = Image.open(img_path)
    pixels = list(img.getdata())
    binary = ''

    for r, g, b in pixels:
        binary += str(r & 1)
        binary += str(g & 1)
        binary += str(b & 1)
        if binary[-16:] == '1111111111111110':
            break

    return bin_to_text(binary[:-16])
