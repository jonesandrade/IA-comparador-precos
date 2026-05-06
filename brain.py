import google.generativeai as genai
import os
import json
import re
from dotenv import load_dotenv

load_dotenv()

# Configuração simples e direta
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def analisar_melhor_opcao(lista_produtos):
    # O modelo 'gemini-1.5-flash' é o mais estável para o plano gratuito atual
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"Analise estes produtos e retorne APENAS um JSON com os campos: nome, preco, link e motivo. Lista: {lista_produtos}"
    
    try:
        response = model.generate_content(prompt)
        texto = response.text
        
        # Busca o JSON dentro da resposta (segurança contra textos extras da IA)
        match = re.search(r'\{.*\}', texto, re.DOTALL)
        if match:
            return json.loads(match.group())
        
        return json.loads(texto.replace('```json', '').replace('```', '').strip())
            
    except Exception as e:
        print(f"Erro no Gemini: {str(e)}")
        return {
            "nome": "Erro na análise",
            "preco": "0",
            "link": "#",
            "motivo": f"Houve um problema: {str(e)}"
        }
