from fastapi import HTTPException, status
from schemas.cifra import Cifrar_Response, Decifrar_Response, Decifrar_Forca_Bruta_Response
import aiohttp
import re

def executar_cifra(texto: str, deslocamento: str) -> Cifrar_Response:
    texto_cifrado = ""

    entrada_valida(texto_claro=texto, deslocamento=deslocamento, mensagemErro="Valide os caracteres utilizados e o número de deslocamento utilizado")

    for char in texto:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            texto_cifrado += chr((ord(char) - base + deslocamento) % 26 + base)
        else:
            texto_cifrado += char

    return Cifrar_Response(textoCifrado=texto_cifrado)

def executar_decifrar(texto_cifrado: str, deslocamento: int) -> Decifrar_Response:
    texto_claro = ""

    for char in texto_cifrado:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            texto_claro += chr((ord(char) - base - deslocamento) % 26 + base)
        else:
            texto_claro += char

    return Decifrar_Response(textoClaro=texto_claro)

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

def entrada_valida(texto_claro: str, deslocamento: int, mensagemErro: str) -> HTTPException:
    if(deslocamento <= 0 or deslocamento > 26):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=mensagemErro
        )

    for char in texto_claro:
        if not re.fullmatch(r"[A-Za-z ]+", char):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"O caractere '{repr(char)}' não é permitido. Use apenas letras sem acento e espaços."
            )