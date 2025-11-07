from pydantic import BaseModel
class Cifrar(BaseModel):
    textoClaro: str
    deslocamento: int

class Cifrar_Response(BaseModel):
    textoCifrado: str

class Decifrar(BaseModel):
    textoCifrado: str
    deslocamento: int

class Decifrar_Response(BaseModel):
    textoClaro: str

class Decifrar_Forca_Bruta(BaseModel):
    textoCifrado: str

class Decifrar_Forca_Bruta_Response(BaseModel):
    textoClaro: str
