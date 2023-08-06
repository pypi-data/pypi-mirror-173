from http.client import ImproperConnectionState
from skimage.io import imread, imsave

def ler_img(caminho, is_gray = False):
    imagem = imread(caminho, as_gray=is_gray)
    return imagem

def slv_img(imagem, caminho):
    imsave(caminho, imagem)