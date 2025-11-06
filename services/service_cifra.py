from fastapi import HTTPException, status
from schemas.cifra import Cifrar_Response, Decifrar_Response

def executar_cifra(texto: str, deslocamento: str) -> Cifrar_Response:
    texto_cifrado = ""

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

def entrada_valida(chave_binario: str, texto_binario: str, mensagemErro: str) -> HTTPException:
    if len(chave_binario) < len(texto_binario):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=mensagemErro
        )