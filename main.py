from fastapi import FastAPI
from scraper import buscar_precos
from brain import analisar_melhor_opcao

app = FastAPI()

@app.get("/")
def home():
    return {"status": "IA de Preços Online"}

@app.get("/buscar")
def pesquisar(nome_produto: str):
    # 1. Coleta os dados brutos da internet
    dados_brutos = buscar_precos(nome_produto)
    
    # 2. IA analisa os dados e escolhe o melhor
    analise_final = analisar_melhor_opcao(dados_brutos)
    
    return {"resultado": analise_final}