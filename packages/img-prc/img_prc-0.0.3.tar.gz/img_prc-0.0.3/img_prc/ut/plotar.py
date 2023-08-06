from turtle import color
import matplotlib.pyplot as plt

def plot_img(imagem):
    plt.figure(figsize=(12,4))
    plt.imshow(imagem, cmap='gray')
    plt.axis('off')
    plt.show()

def plot_resultado(*args):
    number_imagens = len(args)
    fig, axis = plt.subplots(nrows=1, ncols=number_imagens, figsize=(12,4))
    names_list = ['Imagem {}'.format(i) for i in range(1, number_imagens)]
    names_list.append('Result')
    for ax, name, imagem in zip (axis, names_list, args):
        ax.set_title(name)
        ax.imshow(imagem, cmap='gray')
        ax.axis('off')
    fig.tight_layout()
    plt.show()

def plotar_hist(imagem):
    fig, axis = plt.subplot(nrows=1, ncols=3, figsize=(12,4), sharex=True, sharey=True)
    color_lst = ['red', 'green', 'blue']
    for index, (ax,color) in enumerate(zip(axis, color_lst)):
        ax.set_title('{} histograma'.format(color.title()))
        ax.hist(imagem[:, :, index].revel(), bins = 256, color = color, alpha = 0.8)
    fig.tight_layout()
    plt.show()