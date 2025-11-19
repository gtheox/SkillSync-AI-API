# SkillSync AI Matchmaking API

## 📋 Sobre o Projeto

Microserviço de **IA Generativa** do projeto **SkillSync**, desenvolvido para a disciplina de **Disruptive Architectures: IoT, IoB & Generative IA**.

Utiliza o modelo **Google Gemini** para realizar matchmaking inteligente entre projetos e perfis de freelancers, analisando compatibilidade de habilidades, experiência e título profissional.

## 🎯 Objetivo

API REST que recebe um projeto e uma lista de perfis de freelancers, retornando análise de compatibilidade gerada por IA:
- **Score de compatibilidade** (0-100) para cada perfil
- **Justificativa** detalhada da análise
- **Ordenação** automática por melhor match

## 👨‍💻 Desenvolvedores

| Nome                           | RM     | GitHub                                          |
| ------------------------------ | ------ | ----------------------------------------------- |
| Gabriel Teodoro Gonçalves Rosa | 555962 | [gtheox](https://github.com/gtheox)             |
| Luka Shibuya                   | 558123 | [lukashibuya](https://github.com/lukashibuya)   |
| Eduardo Giovannini             | 555030 | [DuGiovannini](https://github.com/DuGiovannini) |

## 🌐 API em Produção

**A API está deployada e disponível online. Use diretamente sem instalação:**

**URL Base:** https://skillsync-ai-api.onrender.com

**Acesse:**
- 📚 [Documentação Interativa](https://skillsync-ai-api.onrender.com/docs) - Teste os endpoints diretamente no navegador
- 🔍 [Health Check](https://skillsync-ai-api.onrender.com/health) - Verifica se a API está online
- 🤖 [Gerar Match](https://skillsync-ai-api.onrender.com/gerar-match) - Endpoint principal de matchmaking

**⚠️ Importante:** No plano gratuito do Render, a primeira requisição após inatividade pode levar 30-60 segundos (serviço "acorda").

## 🏗️ Arquitetura

```
App Mobile (React Native) → API .NET → API de IA (Este microserviço)
```

**Importante**: Este serviço **NÃO** se conecta ao banco de dados. É uma API "pura" que processa texto e retorna JSON.

## 🤖 Arquitetura da IA

### Modelo Escolhido: Google Gemini 2.5 Flash

**Razão da escolha:**
- **Performance**: Balanceamento ideal entre velocidade e qualidade de resposta
- **Capacidade JSON**: Suporte nativo para geração de JSON estruturado via `response_mime_type`
- **Custo**: Modelo eficiente para uso em produção
- **Confiabilidade**: Respostas consistentes e previsíveis

**Configuração:**
```python
model = genai.GenerativeModel(
    model_name='gemini-2.5-flash',
    generation_config={"response_mime_type": "application/json"}
)
```

### Prompt Engineering

O prompt foi estruturado em **4 camadas** para garantir resultados consistentes:

1. **Contexto e Papel** (linhas 77-79)
   - Define o assistente como especialista em RH
   - Estabelece o contexto da plataforma SkillSync

2. **Instruções de Análise** (linhas 87-92)
   - Critérios específicos de avaliação:
     - Compatibilidade de habilidades
     - Relevância do título profissional
     - Adequação do resumo/experiência
     - Alinhamento geral com o projeto

3. **Sistema de Pontuação** (linhas 94-99)
   - Escala clara e objetiva de 0-100
   - Faixas bem definidas para cada nível de compatibilidade
   - Facilita a interpretação dos resultados

4. **Formato de Resposta** (linhas 103-113)
   - Instruções rígidas para garantir JSON válido
   - Prevenção de markdown ou texto extra
   - Validação de campos obrigatórios

### Processamento Assíncrono

A API utiliza `ThreadPoolExecutor` para executar chamadas síncronas do Gemini de forma assíncrona, garantindo:
- **Performance**: Não bloqueia outras requisições
- **Escalabilidade**: Suporta múltiplas requisições simultâneas
- **Eficiência**: Aproveitamento otimizado de recursos

### Validação e Tratamento de Erros

- **Validação de Entrada**: Pydantic valida automaticamente o formato dos dados
- **Validação de Saída**: Verificação de estrutura JSON e campos obrigatórios
- **Limpeza de Resposta**: Remoção automática de markdown code blocks
- **Normalização**: Garantia de scores entre 0-100
- **Ordenação**: Matches ordenados por score (maior primeiro)

## 🛠️ Tecnologias

- **Python 3.8+** - Linguagem principal
- **FastAPI** - Framework web moderno e assíncrono para APIs REST
- **Google Generative AI (Gemini 2.5 Flash)** - Modelo de IA Generativa
- **Pydantic** - Validação de dados e serialização
- **python-dotenv** - Gerenciamento de variáveis de ambiente
- **Uvicorn** - Servidor ASGI de alta performance

## 📦 Instalação

### 1. Criar ambiente virtual

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```powershell
python -m venv venv
venv\Scripts\activate
```

### 2. Instalar dependências

```bash
pip install -r requirements.txt
```

### 3. Configurar chave da API

Crie o arquivo `.env` a partir do exemplo:
```bash
cp .env.example .env
```

Edite o `.env` e adicione sua chave:
```
GOOGLE_AI_KEY=sua_chave_aqui
```

Obtenha sua chave em: https://makersuite.google.com/app/apikey

## 🚀 Execução Local (Opcional)

Se preferir rodar localmente:

```bash
python main.py
```

A API local estará disponível em:
- **API**: http://127.0.0.1:8000
- **Documentação**: http://127.0.0.1:8000/docs
- **Health Check**: http://127.0.0.1:8000/health

## 📡 Endpoints

### GET /health

Verifica se a API está online.

**Resposta:**
```json
{"status": "ok"}
```

### POST /gerar-match

Analisa compatibilidade entre projeto e perfis usando IA Generativa.

**Request:**
```json
{
  "projeto": {
    "titulo": "Desenvolvimento de App Mobile",
    "descricao": "Preciso de um desenvolvedor React Native..."
  },
  "perfis": [
    {
      "id_perfil": 1,
      "titulo_profissional": "Desenvolvedor Mobile Senior",
      "resumo": "5 anos de experiência em React Native...",
      "habilidades": ["React Native", "JavaScript", "TypeScript"]
    }
  ]
}
```

**Response:**
```json
{
  "matches": [
    {
      "id_perfil": 1,
      "score_compatibilidade": 95,
      "justificativa": "Perfil altamente compatível..."
    }
  ]
}
```

## 🔗 Integração com API .NET

A API .NET deve fazer uma requisição HTTP POST para a API em produção:

```csharp
var client = new HttpClient();
var response = await client.PostAsJsonAsync(
    "https://skillsync-ai-api.onrender.com/gerar-match", 
    request
);
var matches = await response.Content.ReadFromJsonAsync<MatchResponse>();
```

**URL de Produção:** `https://skillsync-ai-api.onrender.com`

**Para desenvolvimento local**, use: `http://localhost:8000`

## 📝 Estrutura do Projeto

```
IA/
├── main.py              # Código principal da API
├── requirements.txt     # Dependências Python
├── .env.example        # Template de variáveis de ambiente
├── .env                # Variáveis de ambiente (configurar localmente)
├── test_api.py         # Script de teste da API
├── .gitignore          # Arquivos ignorados pelo Git
└── README.md           # Documentação
```

## ⚠️ Troubleshooting

### Erro: "GOOGLE_AI_KEY não encontrada"
- Verifique se o arquivo `.env` existe
- Confirme que a chave está no formato: `GOOGLE_AI_KEY=sua_chave` (sem espaços)

### Erro: "Address already in use"
- A porta 8000 está em uso
- Encerre o processo: `lsof -ti:8000 | xargs kill`
- Ou use outra porta: `uvicorn main:app --port 8001`

### Erro: "Erro ao configurar a API do Gemini"
- Verifique se a chave está correta
- Confirme que a chave não expirou

## 🎥 Vídeo de Apresentação

📹 **[Assista ao vídeo de demonstração](https://youtu.be/NBnWwr5bF-M)**

[![Assista ao vídeo](https://img.youtube.com/vi/NBnWwr5bF-M/0.jpg)](https://youtu.be/NBnWwr5bF-M)

## 📚 Documentação Adicional

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Google Generative AI](https://ai.google.dev/)

---

**Desenvolvido para a Global Solution**
