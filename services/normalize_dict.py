import unicodedata
import os

def normalizar_dicionario():
    caminho_arquivo = "../dictionary/new_dict.dic"
    pasta, nome = os.path.split(caminho_arquivo)
    nome_sem_extensao, ext = os.path.splitext(nome)
    novo_nome = f"{nome_sem_extensao}_normalizado{ext}"
    caminho_novo = os.path.join(pasta, novo_nome)

    palavras_normalizadas = set()

    with open(caminho_arquivo, "r", encoding="utf-8") as f:
        for linha in f:
            palavra = linha.strip().lower()
            if not palavra:
                continue

            palavra_normalizada = unicodedata.normalize("NFD", palavra)
            palavra_normalizada = "".join(
                c for c in palavra_normalizada if unicodedata.category(c) != "Mn"
            )

            if palavra_normalizada.isalpha():
                palavras_normalizadas.add(palavra_normalizada)

    with open(caminho_novo, "w", encoding="utf-8") as f:
        for palavra in sorted(palavras_normalizadas):
            f.write(palavra + "\n")

    print(f"Dicionário normalizado salvo em: {caminho_novo}")


normalizar_dicionario()
