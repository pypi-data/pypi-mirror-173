# Importando bibliotecas
import os 'sistema operacional'

def sentinel_sen2cor():
    # criar lista com as pastas das imagens sentinel2
    lista_sentinel = [pasta for pasta in os.listdir() if "SAFE" in pasta]
    print(lista_sentinel)

    # excutar sen2cor em loop
    for img in lista_sentinel:
        if "MSIL2A" not in img:
            sen2cor = f"Sen2Cor\\L2A_Process.bat {img}"
            os.system(sen2cor)
            print(f'### Imagem {img} corrigida ###')
