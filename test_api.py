"""
Script de teste para a API SkillSync-Matcher
Execute após iniciar o servidor: python test_api.py
"""

import requests
import json

# URL base da API (ajuste se necessário)
BASE_URL = "http://127.0.0.1:8000"

def test_health():
    """Testa o endpoint de health check"""
    print("🔍 Testando GET /health...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"✅ Status: {response.status_code}")
        print(f"✅ Resposta: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def test_gerar_match():
    """Testa o endpoint de geração de matches"""
    print("\n🔍 Testando POST /gerar-match...")
    
    # Dados de teste
    payload = {
        "projeto": {
            "titulo": "Desenvolvimento de App Mobile React Native",
            "descricao": "Preciso de um desenvolvedor React Native experiente para criar um aplicativo de delivery com integração de pagamento via Stripe, autenticação de usuários e sistema de notificações push."
        },
        "perfis": [
            {
                "id_perfil": 1,
                "titulo_profissional": "Desenvolvedor Mobile Senior",
                "resumo": "5 anos de experiência em React Native, especializado em apps de e-commerce e integração de pagamentos. Já desenvolvi mais de 10 apps publicados nas stores.",
                "habilidades": ["React Native", "JavaScript", "TypeScript", "Firebase", "Stripe", "Redux", "Node.js"]
            },
            {
                "id_perfil": 2,
                "titulo_profissional": "Designer UX/UI",
                "resumo": "Designer com foco em interfaces mobile e web. Experiência em prototipação e design systems.",
                "habilidades": ["Figma", "Adobe XD", "UI Design", "Prototipação", "Design Systems"]
            },
            {
                "id_perfil": 3,
                "titulo_profissional": "Desenvolvedor Full Stack",
                "resumo": "Desenvolvedor com experiência em React Native e backend Node.js. Conhece integração de APIs e sistemas de pagamento.",
                "habilidades": ["React Native", "Node.js", "MongoDB", "REST API", "JavaScript"]
            }
        ]
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/gerar-match",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"✅ Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Matches encontrados: {len(result['matches'])}")
            print("\n📊 Resultados:")
            for match in result['matches']:
                print(f"  - Perfil {match['id_perfil']}: Score {match['score_compatibilidade']}/100")
                print(f"    Justificativa: {match['justificativa']}")
            return True
        else:
            print(f"❌ Erro: {response.status_code}")
            print(f"❌ Resposta: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("🧪 TESTE DA API SKILLSYNC-MATCHER")
    print("=" * 60)
    
    # Testa health check
    health_ok = test_health()
    
    if health_ok:
        # Testa geração de matches
        test_gerar_match()
    else:
        print("\n⚠️  Servidor não está respondendo. Certifique-se de que a API está rodando.")
        print("   Execute: python main.py ou uvicorn main:app --reload")
    
    print("\n" + "=" * 60)

