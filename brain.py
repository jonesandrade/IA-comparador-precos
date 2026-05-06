import google.generativeai as genai
import os
import json
import re
from dotenv import load_dotenv

load_dotenv()

# Forçamos a configuração básica
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def analisar_melhor_opcao(lista_produtos):
    # Usamos o 1.5-flash que é o mais compatível com contas gratuitas hoje
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"Analise estes produtos e retorne APENAS um JSON com nome, preco, link e motivo: {lista_produtos}"
    
    try:
        # Adicionamos um safety_settings simples para evitar bloqueios bobos
        response = model.generate_content(prompt)
        texto = response.text
        
        match = re.search(r'\{.*\}', texto, re.DOTALL)
        if match:
            return json.loads(match.group())
        
        return json.loads(texto.replace('```json', '').replace('```', '').strip())
            
    except Exception as e:
        print(f"Erro no Gemini: {str(e)}")
        return {
            "nome": "Erro de Conexão",
            "preco": "---",
            "link": "#",
            "motivo": f"A API do Google retornou: {str(e)}. Verifique se a sua chave API é do 'Google AI Studio'."
        }
