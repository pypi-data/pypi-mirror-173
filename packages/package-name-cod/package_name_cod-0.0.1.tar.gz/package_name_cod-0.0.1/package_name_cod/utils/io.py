from skimage.io import imread,imsave

def imagem_pronta(path, is_gray = False):
    imagem = imread(path, as_gray = is_gray)
    return imagem

def salvar_imagem(imagem, path):
    imsave(path, imagem)
