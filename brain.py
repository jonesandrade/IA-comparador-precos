import google.generativeai as genai
import os
import json
import re
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def analisar_melhor_opcao(lista_produtos):
    # 'gemini-pro' é o nome mais estável e universal para evitar o erro 404
    model = genai.GenerativeModel('gemini-pro')
    
    prompt = f"""
    Atue como um analista de compras. Analise os produtos abaixo e escolha o melhor custo-benefício.
    Retorne APENAS um objeto JSON puro com os campos: "nome", "preco", "link" e "motivo".
    
    Lista: {lista_produtos}
    """
    
    try:
        response = model.generate_content(prompt)
        texto = response.text
        
        # Tenta extrair o JSON se a IA mandar texto extra
        match = re.search(r'\{.*\}', texto, re.DOTALL)
        if match:
            return json.loads(match.group())
        
        return json.loads(texto.replace('```json', '').replace('```', '').strip())
            
    except Exception as e:
        print(f"Erro no Gemini: {str(e)}")
        # Retorno de segurança para o seu HTML não exibir "Erro ao buscar"
        return {
            "nome": "Produto não analisado",
            "preco": "Ver no site",
            "link": "#",
            "motivo": f"Erro na IA: {str(e)}"
        }
