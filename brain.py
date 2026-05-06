import google.generativeai as genai
import os
import json
import re
from google.generativeai.types import RequestOptions
from dotenv import load_dotenv

load_dotenv()

# Configuração com RequestOptions para tentar contornar o erro de versão
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def analisar_melhor_opcao(lista_produtos):
    # Vamos tentar o modelo 'models/gemini-1.5-flash' (nome completo)
    model = genai.GenerativeModel('models/gemini-1.5-flash')
    
    prompt = f"Analise e retorne apenas um JSON com os campos nome, preco, link e motivo: {lista_produtos}"
    
    try:
        # RequestOptions pode ajudar se o problema for a rota da API no servidor
        response = model.generate_content(
            prompt,
            request_options=RequestOptions(api_version='v1')
        )
        
        texto = response.text
        match = re.search(r'\{.*\}', texto, re.DOTALL)
        if match:
            return json.loads(match.group())
        
        return json.loads(texto.replace('```json', '').replace('```', '').strip())
            
    except Exception as e:
        print(f"Erro no Gemini: {str(e)}")
        return {
            "nome": "Erro de Modelo",
            "preco": "---",
            "link": "#",
            "motivo": f"O modelo não foi encontrado (404). Erro: {str(e)}"
        }
