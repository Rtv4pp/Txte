import requests
import cv2
import numpy as np
from bs4 import BeautifulSoup
import json

# Defina a URL base da busca
url_base = "https://www.google.com/search?q={termo}&tbm=isch&tbo=u&source=univ&sa=X&ved=0ahUKEwi1v6CtjJLxAhVEyDgGHQaKDRoQsAQI4gE&biw=1366&bih=657"

# Solicite que o usuário digite o termo de busca
termo = input("Digite o termo de busca: ")

# Substitua os espaços por sinal de mais (+)
termo_formatado = termo.replace(" ", "+")

# Substitua o termo na URL base
url_busca = url_base.format(termo=termo_formatado)

# Faça a requisição HTTP para a página de busca
resposta = requests.get(url_busca)

# Verifique se a busca foi bem-sucedida
if resposta.status_code == 200:

    # Parseie o HTML da página de busca
    soup = BeautifulSoup(resposta.text, "html.parser")

    # Encontre todas as imagens na página de busca
    imagens = soup.select('img[src^="http"]')

    # Para cada imagem, verifique se ela contém um rosto de pessoa
    for imagem in imagens:

        # Faça a requisição HTTP para a imagem
        imagem_url = imagem["src"]
        resposta_imagem = requests.get(imagem_url, stream=True)

        # Converta a imagem para um array NumPy
        imagem_array = np.asarray(bytearray(resposta_imagem.content), dtype=np.uint8)
        imagem_opencv = cv2.imdecode(imagem_array, -1)

        # Detecte faces na imagem usando o classificador Haar Cascade
        classificador = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        faces = classificador.detectMultiScale(imagem_opencv, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Se a imagem contém pelo menos uma face, imprima o link da imagem
        if len(faces) > 0:
            print("Imagem relacionadas: " + imagem_url)

    def coletar_info_facebook(termo):
        url = f"https://www.facebook.com/search/people/?q={termo}"
        resposta = requests.get(url)
        if resposta.status_code == 200:
            soup = BeautifulSoup(resposta.text, "html.parser")
            resultados = soup.select('div[data-testid="browse-result-content"]')
            for resultado in resultados:
                nome_resultado = resultado.select_one('div[data-testid="browse-result-name"]').text
                perfil_url = resultado.select_one('a[data-testid="browse-result-link"]')['href']
                print(f"Nome: {nome_resultado} | Perfil: {perfil_url}")
        else:
            print("Não foi possível conectar ao Facebook.")


    def coletar_info_instagram(termo):
        url = f"https://www.instagram.com/web/search/topsearch/?query={termo}"
        resposta = requests.get(url)
        if resposta.status_code == 200:
            resultados = json.loads(resposta.text)['users']
            for resultado in resultados:
                nome_resultado = resultado['user']['full_name']
                perfil_url = f"https://www.instagram.com/{resultado['user']['username']}"
                print(f"Nome: {nome_resultado} | Perfil: {perfil_url}")
        else:
            print("Não foi possível conectar ao Instagram.")


    termo_formatado = termo.replace(" ", "+")
    coletar_info_instagram(termo_formatado)
    coletar_info_facebook(termo_formatado)
else:
    print("A busca não foi bem-sucedida. Status code:", resposta.status_code)