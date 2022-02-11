
import random
import string
from captcha.image import ImageCaptcha

# chr_all = string.ascii_letters + string.digits
# chr_4 = ''.join(random.sample(chr_all, 4))
# image = ImageCaptcha().generate_image(chr_4)
# image.save('./%s.jpg' % chr_4)


def random_color(start, end, opacity=None):
    red = random.randint(start, end)
    green = random.randint(start, end)
    blue = random.randint(start, end)
    if opacity is None:
        return red, green, blue
    return red, green, blue, opacity


# 自动生成4位随机校验码 返回图片对象和码值
def check_code():
    background = random_color(238, 255)
    color = random_color(10, 200, random.randint(220, 255))
    chr_all = string.ascii_letters + string.digits
    chr_4 = ''.join(random.sample(chr_all, 4))
    # image = ImageCaptcha(width=120, height=30, font_sizes=[25]).generate_image(chr_4)
    image = ImageCaptcha(width=120, height=40, font_sizes=[25]).create_captcha_image(chr_4, color, background)
    image = ImageCaptcha(width=120, height=40, font_sizes=[25]).create_noise_dots(image, color=color, width=5, number=10)
    return image, chr_4
