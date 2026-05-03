import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def analisar_melhor_opcao(lista_produtos):
    # Mudamos para 'gemini-1.5-flash-latest' que é o nome oficial mais estável
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    
    prompt = f"""
    Atue como um analista de compras brasileiro. Analise os produtos abaixo e escolha o melhor custo-benefício.
    Retorne APENAS um objeto JSON puro, sem blocos de código (Markdown), contendo exatamente os campos:
    "nome", "preco", "link" e "motivo".
    
    Lista: {lista_produtos}
    """
    
    try:
        response = model.generate_content(prompt)
        # Limpa possíveis formatações que a IA coloca como ```json ... ```
        texto_limpo = response.text.replace('```json', '').replace('```', '').strip()
        return json.loads(texto_limpo)
    except Exception as e:
        print(f"Erro detalhado: {str(e)}") # Isso ajuda a ver o erro no log do Render
        return {"nome": "Erro", "preco": "0", "link": "#", "motivo": f"A IA falhou: {str(e)}"}
