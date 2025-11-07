from fastapi import HTTPException, status
from schemas.cifra import Cifrar_Response, Decifrar_Response
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