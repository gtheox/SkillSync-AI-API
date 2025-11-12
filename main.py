import uvicorn
import google.generativeai as genai
import json
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List
from dotenv import load_dotenv
import asyncio
from concurrent.futures import ThreadPoolExecutor

# --- 1. CONFIGURAÇÃO ---
# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Obtém a chave da API do Google Gemini de variável de ambiente
GOOGLE_AI_KEY = os.getenv("GOOGLE_AI_KEY")

if not GOOGLE_AI_KEY:
    raise ValueError(
        "GOOGLE_AI_KEY não encontrada. "
        "Por favor, defina a variável de ambiente GOOGLE_AI_KEY ou crie um arquivo .env."
    )

try:
    genai.configure(api_key=GOOGLE_AI_KEY)
except Exception as e:
    raise RuntimeError(f"Erro ao configurar a API do Gemini: {e}")

# Thread pool para executar chamadas síncronas do Gemini de forma assíncrona
executor = ThreadPoolExecutor(max_workers=5)

# --- 2. DEFINIÇÃO DOS MODELOS DE DADOS (Contrato da API) ---
# O FastAPI usa Pydantic para validar automaticamente o JSON de entrada e saída.

class Projeto(BaseModel):
    titulo: str
    descricao: str

class Perfil(BaseModel):
    id_perfil: int
    titulo_profissional: str
    resumo: str
    habilidades: List[str]

# Este é o JSON que nossa API .NET vai enviar
class MatchRequest(BaseModel):
    projeto: Projeto
    perfis: List[Perfil]

# Este é o formato de cada item que a IA vai devolver
class MatchResponseItem(BaseModel):
    id_perfil: int
    score_compatibilidade: int = Field(..., ge=0, le=100) # Garante que o score esteja entre 0-100
    justificativa: str

# Este é o JSON final que nossa API de IA vai retornar para o .NET
class MatchResponse(BaseModel):
    matches: List[MatchResponseItem]

# --- 3. INICIALIZAÇÃO DA API ---
app = FastAPI(
    title="SkillSync AI Matchmaking API",
    description="Microserviço de IA Generativa para fazer match entre projetos e freelancers.",
    version="1.0.0"
)

# --- 4. ENGENHARIA DE PROMPT (O "Cérebro" da IA) ---
# Esta função monta a instrução para o Gemini
def criar_prompt_matchmaking(request: MatchRequest) -> str:
    
    # Converte os dados de input em strings JSON para o prompt
    projeto_str = request.projeto.model_dump_json(indent=2)
    perfis_str = json.dumps([p.model_dump() for p in request.perfis], indent=2)

    # Este é o prompt que cumpre o requisito de "Prompt Engineering"
    return f"""Você é um assistente de RH especialista em recrutamento de freelancers para a plataforma SkillSync.

Sua tarefa é analisar um PROJETO e uma LISTA DE PERFIS de freelancers, e calcular a compatibilidade de cada perfil com o projeto.

PROJETO:
{projeto_str}

LISTA DE PERFIS:
{perfis_str}

INSTRUÇÕES DE ANÁLISE:
1. Para CADA perfil na lista, analise:
   - Compatibilidade das habilidades listadas com os requisitos do projeto
   - Relevância do título profissional
   - Adequação do resumo/experiência descrita
   - Alinhamento geral com o escopo do projeto

2. Atribua um score_compatibilidade de 0 a 100 para cada perfil:
   - 90-100: Perfil altamente compatível, atende todos os requisitos principais
   - 70-89: Perfil compatível, atende a maioria dos requisitos
   - 50-69: Perfil parcialmente compatível, pode atender com adaptações
   - 30-49: Perfil pouco compatível, falta experiência/habilidades importantes
   - 0-29: Perfil incompatível, não atende aos requisitos do projeto

3. Escreva uma justificativa curta (1-2 frases) explicando o score atribuído.

FORMATO DE RESPOSTA OBRIGATÓRIO:
Você DEVE retornar APENAS um objeto JSON válido, sem nenhum texto adicional, sem markdown, sem comentários.
O JSON deve seguir EXATAMENTE este formato:

{{"matches": [{{"id_perfil": <número>, "score_compatibilidade": <número 0-100>, "justificativa": "<texto>"}}, ...]}}

IMPORTANTE: 
- Retorne APENAS o JSON, sem ```json ou qualquer outro texto
- Inclua TODOS os perfis da lista, mesmo que tenham score baixo
- Os campos devem ser exatamente: id_perfil, score_compatibilidade, justificativa
- score_compatibilidade deve ser um número inteiro entre 0 e 100"""

# --- 5. O ENDPOINT DA API ---
# Este é o único endpoint do nosso microserviço
@app.post("/gerar-match", response_model=MatchResponse)
async def gerar_match(request: MatchRequest):
    """
    Recebe um Projeto e uma Lista de Perfis, e retorna os matches
    gerados pela IA Generativa (Gemini).
    """
    
    print("Recebida nova requisição de match...") # Log para o console

    # 1. Criar o Prompt
    prompt = criar_prompt_matchmaking(request)
    
    # 2. Configurar o modelo
    try:
        model = genai.GenerativeModel(
            model_name='gemini-2.5-flash', # Modelo disponível na API
            generation_config={"response_mime_type": "application/json"} # Força a saída em JSON!
        )
    except Exception as e:
        print(f"Erro ao carregar o modelo Gemini: {e}")
        raise HTTPException(status_code=500, detail="Erro ao carregar o modelo de IA.")

    # 3. Chamar a IA Generativa (executando de forma assíncrona)
    raw_text = ""  # Inicializa para evitar erro em caso de exceção
    try:
        print("Enviando prompt para o Gemini...")
        
        # Executa a chamada síncrona do Gemini em um thread pool
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(executor, model.generate_content, prompt)
        
        # 4. Processar a resposta da IA
        # O modelo já deve retornar JSON puro graças ao 'response_mime_type'
        if not response or not hasattr(response, 'text'):
            raise ValueError("Resposta inválida do modelo Gemini")
        raw_text = response.text.strip()
        
        # Remove possíveis markdown code blocks se existirem
        if raw_text.startswith("```json"):
            raw_text = raw_text[7:]  # Remove ```json
        if raw_text.startswith("```"):
            raw_text = raw_text[3:]  # Remove ```
        if raw_text.endswith("```"):
            raw_text = raw_text[:-3]  # Remove ```
        raw_text = raw_text.strip()
        
        # 5. Converter o texto (string) em um objeto JSON (dicionário Python)
        json_response = json.loads(raw_text)
        
        # 6. Validar que a resposta tem o formato esperado
        if "matches" not in json_response:
            raise ValueError("Resposta da IA não contém o campo 'matches'")
        
        # 7. Validar e ordenar matches por score (maior primeiro)
        matches = json_response["matches"]
        for match in matches:
            if "score_compatibilidade" not in match or "id_perfil" not in match or "justificativa" not in match:
                raise ValueError("Formato de match inválido na resposta da IA")
            # Garante que o score está entre 0-100
            match["score_compatibilidade"] = max(0, min(100, int(match["score_compatibilidade"])))
        
        # Ordena por score (maior primeiro)
        matches.sort(key=lambda x: x["score_compatibilidade"], reverse=True)
        
        print(f"Match recebido do Gemini: {len(matches)} perfis analisados com sucesso.")
        return MatchResponse(matches=[MatchResponseItem(**match) for match in matches])

    except json.JSONDecodeError as e:
        error_msg = f"Erro: A IA não retornou um JSON válido."
        if raw_text:
            error_msg += f" Resposta recebida: {raw_text[:200]}..."  # Limita a 200 chars
        print(error_msg)
        raise HTTPException(
            status_code=500, 
            detail=f"A resposta da IA não era um JSON válido: {str(e)}"
        )
    except ValueError as e:
        print(f"Erro de validação: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao processar resposta da IA: {str(e)}")
    except Exception as e:
        print(f"Erro inesperado ao chamar a API do Gemini: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno do servidor de IA: {str(e)}")

# --- 6. ROTA DE HEALTH CHECK ---
# Boa prática para o .NET saber se a API de IA está "viva"
@app.get("/health")
def health_check():
    return {"status": "ok"}

# --- 7. RODAR LOCALMENTE ---
# Execute com: python main.py ou uvicorn main:app --reload
if __name__ == "__main__":
    print("🚀 Iniciando servidor FastAPI local em http://127.0.0.1:8000")
    print("📚 Documentação interativa disponível em http://127.0.0.1:8000/docs")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)