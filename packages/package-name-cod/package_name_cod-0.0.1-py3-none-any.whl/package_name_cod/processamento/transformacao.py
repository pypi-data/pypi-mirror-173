from skimage.transform import resize

def redimensionar_imagem(imagem , proporcao):
    assert 0 <= proporcao <=1, "Especifique a proporcao (entre 0 e 1)."
    height = round(imagem.shape[0] * proporcao)
    width = round(imagem.shape[1] * proporcao)
    image_resized = resize(imagem (height, width), anti_aliasing=True)
    return image_resized
