from email.mime import image
from skimage.io import imread, imsave

# Fazendo a leitur da imagem
def read_image(path, is_gray = False):
    image = imread(path, as_gray= is_gray)
    return image

# Salvando o imagem
def sava_image(image, path):
    imsave(path, image)