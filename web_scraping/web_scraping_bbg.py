import requests
import os

def url_json(objec_id: int, page_id: int) -> str:
    return f'https://api.geekdo.com/api/images?ajax=1&gallery=all&nosession=1&objectid={objec_id}&objecttype=thing&showcount=50&pageid={page_id}'

def dowload_lista_url_page(objec_id: int, page_id: int) -> list[str]:
    response = requests.get(url_json(objec_id,page_id)).json()
    total = int(response['pagination']['total'])
    lista = [img['imageurl_lg'] for img in response['images']]
    return total, lista 

def dowload_lista_url(objec_id: int) -> list[str]:    
    page_id = 1
    total, image_urls = dowload_lista_url_page(objec_id, page_id)
       
    while page_id*50 < total:
        page_id += 1
        _, lista = dowload_lista_url_page(objec_id, page_id)
        image_urls += lista

    return image_urls


def download_imagem(url, output_folder):
    try:
        response = requests.get(url)
        if response.status_code == 200:           
            filename = os.path.join(output_folder, url.split("/")[-1])           
            with open(filename, 'wb') as f:
                f.write(response.content)           
        else:
            print(f"ERRO: {url} (Status Code: {response.status_code})")
    except Exception as e:
        print(f"ERRO {url}: {str(e)}")

def download_imagens(objec_id, output_folder):   
    os.makedirs(output_folder, exist_ok=True)
    try:       
        image_urls = dowload_lista_url(objec_id)
        total = len(image_urls)
        for i, url in enumerate(image_urls):
            print(f'{output_folder}: {i+1}/{total}')
            download_imagem(url, output_folder)
        print("Download concluído")
    except Exception as e:
        print(f"ERRO: {str(e)}")

if __name__ == '__main__':
    download_imagens(224517,'dataset/brass_birmingham')
    download_imagens(161936,'dataset/pandemic')
    download_imagens(174430,'dataset/gloomhaven')
    download_imagens(342942,'dataset/ark_nova')
    download_imagens(233078,'dataset/twilight_imperium')
    download_imagens(167791,'dataset/terraforming_mars')