from fastapi import APIRouter
from schemas.cifra import Cifrar, Cifrar_Response, Decifrar, Decifrar_Response
from services.service_cifra import executar_cifra, executar_decifrar

router = APIRouter()

@router.post("/cifrar", response_model=Cifrar_Response)
def cifrar(input: Cifrar):
    return executar_cifra(input.textoClaro, input.deslocamento)

@router.post("/decifrar", response_model=Decifrar_Response)
def decifrar(input: Decifrar):
    return executar_decifrar(input.textoCifrado, input.deslocamento)