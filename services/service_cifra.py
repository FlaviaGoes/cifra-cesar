from fastapi import HTTPException, status
from schemas.cifra import Cifrar_Response, Decifrar_Response, Decifrar_Forca_Bruta_Response
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
    if not palavra or palavra.strip() == "":
        return "Não há texto para ser decifrado."
    
    with open("dictionary/new_dict_normalizado.dic", "r", encoding="utf-8") as f:
        dicionario = set(linha.strip() for linha in f if linha.strip())

    palavras_cifradas = [pv.lower() for pv in palavra.strip().split()]
    total_palavras = len(palavras_cifradas)
    
    palavras_checagem = palavras_cifradas if total_palavras > 3 else palavras_cifradas[:3]

    for deslocamento in range(1, 27):
        palavras_validas_encontradas = 0

        for palavra_teste in palavras_checagem:
            resposta = executar_decifrar(palavra_teste, deslocamento)
            palavra_decifrada = resposta.textoClaro.strip().lower()

            if not palavra_decifrada:
                continue

            if palavra_decifrada in dicionario:
                palavras_validas_encontradas += 1

        if palavras_validas_encontradas > 0:
            decifrado_completo = executar_decifrar(palavra, deslocamento).textoClaro
            return decifrado_completo

    return "Nenhuma decifração válida encontrada."

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