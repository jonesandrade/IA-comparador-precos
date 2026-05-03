from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from scraper import buscar_precos
from brain import analisar_melhor_opcao
import os

app = FastAPI()

# Faz o FastAPI enxergar a pasta 'static'
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def home():
    # Retorna o painel visual
    return FileResponse("static/index.html")

@app.get("/buscar")
def pesquisar(nome_produto: str):
    dados_brutos = buscar_precos(nome_produto)
    analise_final = analisar_melhor_opcao(dados_brutos)
    return {"resultado": analise_final}
