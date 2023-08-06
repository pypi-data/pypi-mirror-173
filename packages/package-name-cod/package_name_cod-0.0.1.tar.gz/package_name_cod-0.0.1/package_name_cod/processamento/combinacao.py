import numpy as np
from skimage.color import rgb2gray
from skimage.exposure import match_histograms
from skimage.metrics import structural_similarity

def encontre_a_diferenca (imagem_1, imagem_2):
   assert imagem_1.shape == imagem_2.shape, "As duas imagens precisam ter o mesmo shape."
   cinza_imagem_1 = rgb2gray(imagem_1)
   cinza_imagem_2 = rgb2gray(imagem_2)  
   (score, difference_image) = structural_similarity(cinza_imagem_1, cinza_imagem_2, full=True)
   print("Similaridade da imagem: ", score)

   return difference_image

def transferir_histograma(imagem_1, imagem_2):
    matched_image = match_histograms (imagem_1, imagem_2, multichannel=True)
    return matched_image

