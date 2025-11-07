from fastapi import HTTPException, status
from schemas.cifra import Cifrar_Response, Decifrar_Response, Decifrar_Forca_Bruta_Response
import aiohttp
import re

def executar_cifra(texto: str, chave: str) -> Cifrar_Response:
    texto_cifrado = ""
    texto_binario = ''.join(format(ord(char), '08b') for char in texto)
    chave_binario = ''.join(format(ord(char), '08b') for char in chave)

    entrada_valida(chave_binario, texto_binario, "A chave informada é menor que o texto e não pode ser utilizada")
        
    for i in range(len(texto_binario)):
        if texto_binario[i] == chave_binario[i]:
            texto_cifrado += '0'
        else:
            texto_cifrado += '1'

    return Cifrar_Response(texto_cifrado=texto_cifrado)

def executar_decifrar(texto_binario: str, chave: str) -> Decifrar_Response:
    chave_binario = ''.join(format(ord(char), '08b') for char in chave)

    entrada_valida(chave_binario, texto_binario, "A chave deve ter o mesmo tamanho ou maior que o texto cifrado.")
    
    texto = ""
    texto_claro = ""

    for i in range(len(texto_binario)):
        if texto_binario[i] == chave_binario[i]:
            texto += '0'
        else:
            texto += '1'

        if len(texto) >= 8:
            texto_claro += ''.join(chr(int(b, 2)) for b in texto.split())
            texto = ''

    return Decifrar_Response(texto_claro=texto_claro)

async def executar_decifrar_forca_bruta(texto_cifrado: str) -> Decifrar_Forca_Bruta_Response:
    resposta = await buscar_palavra(texto_cifrado)
    return Decifrar_Forca_Bruta_Response(textoClaro=resposta)

async def buscar_palavra(palavra: str):
    url = f"https://api.dicionario-aberto.net/word/{palavra}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resposta:
            if resposta.status != 200:
                return f"Erro: Falha ao consultar API (status {resposta.status})"

            dados = await resposta.json()

            print(dados)

            if isinstance(dados, list) and len(dados) > 0 and "xml" in dados[0]:
                xml_texto = dados[0]["xml"]

                definicoes = re.findall(r"<orth>(.*?)</orth>", xml_texto, re.DOTALL)

                if definicoes:
                    definicao_limpa = re.sub(r"<.*?>", "", definicoes[0]).strip()
                    return definicao_limpa

                return "Definição não encontrada no XML."
            else:
                return "Nenhuma definição encontrada."

def entrada_valida(chave_binario: str, texto_binario: str, mensagemErro: str) -> HTTPException:
    if len(chave_binario) < len(texto_binario):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=mensagemErro
        )