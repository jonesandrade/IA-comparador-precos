import google.generativeai as genai
import os
import json
import re
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def analisar_melhor_opcao(lista_produtos):
    # Alterado para 'gemini-1.5-pro', que possui maior compatibilidade em diferentes regiões
    model = genai.GenerativeModel('gemini-1.5-pro')
    
    prompt = f"""
    Atue como um analista de compras brasileiro. Analise os produtos abaixo e escolha o melhor custo-benefício.
    Retorne APENAS um objeto JSON puro, sem blocos de código ou explicações.
    Campos obrigatórios: "nome", "preco", "link" e "motivo".
    
    Lista: {lista_produtos}
    """
    
    try:
        response = model.generate_content(prompt)
        texto = response.text
        
        # Expressão regular para extrair apenas o conteúdo entre chaves { }
        # Isso evita erros se a IA responder com ```json ou textos extras
        match = re.search(r'\{.*\}', texto, re.DOTALL)
        if match:
            json_str = match.group()
            return json.loads(json_str)
        else:
            # Caso a IA não retorne um JSON válido
            return json.loads(texto.replace('```json', '').replace('```', '').strip())
            
    except Exception as e:
        print(f"Erro detalhado no brain.py: {str(e)}")
        return {
            "nome": "Erro na análise",
            "preco": "0",
            "link": "#",
            "motivo": f"Houve um problema técnico com a IA: {str(e)}"
        }
