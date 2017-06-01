from PIL import Image


def count_nums(img):
    img = Image.open(img)
    nums = []
    for numy in range(0, 6):
        for numx in range(0, 8):
            box = (0 + 111*numx, 0 + 111*numy, 0 + 111*numx + 111, 0 + 111*numy + 111)
            num_img = img.crop(box)
            colors = num_img.getcolors()
            if len(colors) > 1:
                nums.append(8 * numy + numx+1)
    return nums
