import google.generativeai as genai
import os
import json
import re
from dotenv import load_dotenv

# Carrega o .env apenas se estiver rodando localmente
load_dotenv()

# Configura a API usando a variável que você acabou de criar no Render
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def analisar_melhor_opcao(lista_produtos):
    # Usamos o modelo flash que é o mais rápido e estável para contas free
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"Analise estes produtos e retorne APENAS um JSON com os campos: nome, preco, link e motivo. Lista: {lista_produtos}"
    
    try:
        response = model.generate_content(prompt)
        texto = response.text
        
        # Filtro para garantir que pegamos apenas o JSON (entre chaves)
        match = re.search(r'\{.*\}', texto, re.DOTALL)
        if match:
            return json.loads(match.group())
        
        # Caso não precise de regex
        return json.loads(texto.replace('```json', '').replace('```', '').strip())
            
    except Exception as e:
        print(f"Erro no Gemini: {str(e)}")
        return {
            "nome": "Erro de análise",
            "preco": "0",
            "link": "#",
            "motivo": f"Houve um problema técnico: {str(e)}"
        }
