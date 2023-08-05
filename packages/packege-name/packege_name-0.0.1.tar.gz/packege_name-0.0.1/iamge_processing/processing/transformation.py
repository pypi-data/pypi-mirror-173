from skimage.transform import resize

# Fazendo a transformação de uma imagem(colocando ela dentro de uma proporção adequada)
def resize_image(image, proportion):
    assert 0 <= proportion <= 1, 'Specify a valid proportion betwen 0 and 1'
    height = round(image.shape[0] * proportion)
    width = round(image.shape[1] * proportion)
    image_resied = resize(image, (height, width), anti_aliasing=True)
    return image_resied
