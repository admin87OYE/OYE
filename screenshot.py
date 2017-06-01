from PIL import ImageGrab


def screenshot(file_dir):
    ImageGrab.grab().save(file_dir, "PNG")
