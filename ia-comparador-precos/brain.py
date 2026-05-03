import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("AIzaSyDr8WAsdPgAYxhky6c9K5l2h70WZFz15cI"))

def analisar_melhor_opcao(lista_produtos):
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""
    Você é um assistente de compras brasileiro. 
    Analise a lista de produtos abaixo e escolha o melhor custo-benefício baseado em preço e avaliação.
    Retorne APENAS um JSON com: nome, preco, link e motivo_escolha.
    
    Lista: {lista_produtos}
    """
    
    response = model.generate_content(prompt)
    return response.text