from email.mime import image
from turtle import width
from skimage.transform import resize

def tam_img(imagem, proporcao):
    assert 0 <= proporcao <= 1, "Especifique uma proporção valida entre 0 e 1"
    heigth = round(imagem.shape[0] * proporcao)
    width = round(imagem.shape[1] * proporcao)
    tam_img = resize(imagem, (heigth, width), anti_aliasing=True)
    return tam_img