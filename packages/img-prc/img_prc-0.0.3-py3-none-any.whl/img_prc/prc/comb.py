from encodings import normalize_encoding
from imp import IMP_HOOK
from msilib.schema import MsiPatchHeaders
from ssl import ALERT_DESCRIPTION_HANDSHAKE_FAILURE
import numpy as np
from skimage.color import rgb2gray
from skimage.exposure import match_histograms
from skimage.metrics import structural_similarity

def enc_dif(imagem1, imagem2):
    assert imagem1.shape == imagem2.shape, "Especifique 2 imagens com o mesma forma"
    gray_imagem1 = rgb2gray(imagem1)
    gray_imagem2 = rgb2gray(imagem2)   
    (score, difference_image) = structural_similarity(gray_imagem1, gray_imagem2, full=True)
    print("Similaridade das imagens: ", score)
    normalized_difference_image = (difference_image-np.min(difference_image))/(np.max(difference_image)-np.min(difference_image))
    return normalized_difference_image

def trnsf_hist(imagem1, imagem2):
    matched_image = match_histograms(imagem1, imagem2, multichannel=True)
    return matched_image