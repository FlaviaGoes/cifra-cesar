from pydantic import BaseModel
class Cifrar(BaseModel):
    texto_claro: str
    chave: str

class Cifrar_Response(BaseModel):
    texto_cifrado: str

class Decifrar(BaseModel):
    texto_cifrado: str
    chave: str

class Decifrar_Response(BaseModel):
    texto_claro: str