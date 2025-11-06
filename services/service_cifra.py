from fastapi import HTTPException, status
from schemas.cifra import Cifrar_Response, Decifrar_Response

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

def entrada_valida(chave_binario: str, texto_binario: str, mensagemErro: str) -> HTTPException:
    if len(chave_binario) < len(texto_binario):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=mensagemErro
        )