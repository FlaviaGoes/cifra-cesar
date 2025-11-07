from fastapi import APIRouter
from schemas.cifra import Cifrar, Cifrar_Response, Decifrar, Decifrar_Response, Decifrar_Forca_Bruta, Decifrar_Forca_Bruta_Response
from services.service_cifra import executar_cifra, executar_decifrar, executar_decifrar_forca_bruta

router = APIRouter(prefix='/cifra', tags=["Cifra"])

@router.post("/cifrar", response_model=Cifrar_Response)
def cifrar(input: Cifrar):
    return executar_cifra(input.texto_claro, input.chave)

@router.post("/decifrar", response_model=Decifrar_Response)
def decifrar(input: Decifrar):
    return executar_decifrar(input.texto_cifrado, input.chave)

@router.post("/decifrarForcaBruta", response_model=Decifrar_Forca_Bruta_Response)
async def decifrarForcaBruta(input: Decifrar_Forca_Bruta):
    return await executar_decifrar_forca_bruta(input.textoCifrado)