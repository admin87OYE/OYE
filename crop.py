from PIL import Image


def crop_image(input_image, output_image, start_x, start_y, width, height):
    """Pass input name image, output name image, x coordinate to start croping, y coordinate to start croping,
     width to crop, height to crop """
    input_img = Image.open(input_image)
    box = (start_x, start_y, start_x + width, start_y + height)
    output_img = input_img.crop(box)
    output_img.save(output_image + ".png")


def main():
    crop_image("Input.png", "output", 0, 0, 1280, 399)

if __name__ == '__main__':
    main()
