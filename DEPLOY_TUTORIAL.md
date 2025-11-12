# 🚀 Tutorial de Deploy - SkillSync AI API

## 📋 Pré-requisitos

- Conta no GitHub (gratuita)
- Conta no Render.com (gratuita)
- Repositório GitHub com o código da API

---

## 🌐 Opção 1: Deploy no Render.com (Recomendado - Gratuito)

### Passo 1: Preparar o Repositório GitHub

1. **Crie um repositório no GitHub** (se ainda não tiver):
   - Acesse: https://github.com/new
   - Nome: `skillsync-ai-api` (ou outro nome)
   - Público ou Privado (sua escolha)
   - Não inicialize com README (já temos um)

2. **Faça commit e push do código**:
   ```bash
   cd /Users/gabrielteodoro/GS/IA
   
   # Inicializar git (se ainda não tiver)
   git init
   
   # Adicionar arquivos
   git add .
   
   # Commit
   git commit -m "Initial commit: SkillSync AI Matchmaking API"
   
   # Conectar ao repositório remoto (substitua USERNAME pelo seu)
   git remote add origin https://github.com/USERNAME/skillsync-ai-api.git
   
   # Push
   git branch -M main
   git push -u origin main
   ```

### Passo 2: Criar Conta no Render.com

1. Acesse: https://render.com
2. Clique em **"Get Started for Free"**
3. Faça login com sua conta GitHub (recomendado)

### Passo 3: Criar Web Service no Render

1. **No Dashboard do Render**, clique em **"New +"** → **"Web Service"**

2. **Conecte seu repositório GitHub**:
   - Se ainda não conectou, autorize o Render a acessar seus repositórios
   - Selecione o repositório `skillsync-ai-api`

3. **Configure o Web Service**:
   
   **Nome:**
   ```
   skillsync-ai-api
   ```
   
   **Região:**
   ```
   Oregon (US West) - ou mais próxima de você
   ```
   
   **Branch:**
   ```
   main
   ```
   
   **Runtime:**
   ```
   Python 3
   ```
   
   **Build Command:**
   ```bash
   pip install -r requirements.txt
   ```
   
   **Start Command:**
   ```bash
   uvicorn main:app --host 0.0.0.0 --port $PORT
   ```
   
   **Plan:**
   ```
   Free (gratuito)
   ```

4. **Configure Environment Variables**:
   - Clique em **"Environment"** na barra lateral
   - Adicione a variável:
     ```
     Key: GOOGLE_AI_KEY
     Value: sua_chave_do_gemini_aqui
     ```
   - Clique em **"Save Changes"**

5. **Deploy**:
   - Clique em **"Create Web Service"**
   - O Render começará a fazer o build automaticamente
   - Aguarde 2-5 minutos para o deploy completar

### Passo 4: Verificar o Deploy

1. **Aguarde o build completar** (você verá logs em tempo real)

2. **Quando o deploy estiver pronto**, você verá:
   ```
   Your service is live at https://skillsync-ai-api.onrender.com
   ```

3. **Teste a API**:
   ```bash
   # Health Check
   curl https://skillsync-ai-api.onrender.com/health
   
   # Deve retornar: {"status":"ok"}
   ```

4. **Acesse a documentação**:
   ```
   https://skillsync-ai-api.onrender.com/docs
   ```

### Passo 5: Configurar URL Customizada (Opcional)

1. No Dashboard do Render, vá em **Settings**
2. Em **"Custom Domain"**, você pode adicionar um domínio próprio
3. Ou use a URL fornecida pelo Render (já funciona perfeitamente)

---

## 🔧 Opção 2: Deploy no Railway (Alternativa Gratuita)

### Passo 1: Criar Conta no Railway

1. Acesse: https://railway.app
2. Faça login com GitHub

### Passo 2: Criar Novo Projeto

1. Clique em **"New Project"**
2. Selecione **"Deploy from GitHub repo"**
3. Escolha seu repositório `skillsync-ai-api`

### Passo 3: Configurar

1. **Railway detecta automaticamente** que é Python
2. Adicione a variável de ambiente:
   ```
   GOOGLE_AI_KEY=sua_chave_aqui
   ```
3. Railway fará o deploy automaticamente

### Passo 4: Obter URL

1. Após o deploy, Railway fornecerá uma URL como:
   ```
   https://skillsync-ai-api-production.up.railway.app
   ```

---

## 🔧 Opção 3: Deploy no Fly.io (Alternativa)

### Passo 1: Instalar Fly CLI

```bash
# Mac
curl -L https://fly.io/install.sh | sh

# Ou via Homebrew
brew install flyctl
```

### Passo 2: Login

```bash
fly auth login
```

### Passo 3: Criar App

```bash
cd /Users/gabrielteodoro/GS/IA
fly launch
```

### Passo 4: Configurar

1. Siga as instruções interativas
2. Adicione a variável de ambiente:
   ```bash
   fly secrets set GOOGLE_AI_KEY=sua_chave_aqui
   ```

### Passo 5: Deploy

```bash
fly deploy
```

---

## 📝 Atualizar README com Link de Deploy

Após fazer o deploy, atualize o README.md com:

```markdown
## 🌐 Deploy

API em produção: https://skillsync-ai-api.onrender.com

- **Documentação**: https://skillsync-ai-api.onrender.com/docs
- **Health Check**: https://skillsync-ai-api.onrender.com/health
```

---

## ✅ Checklist de Deploy

- [ ] Código commitado e pushado no GitHub
- [ ] Conta criada no Render.com (ou alternativa)
- [ ] Web Service criado
- [ ] Variável `GOOGLE_AI_KEY` configurada
- [ ] Build completado com sucesso
- [ ] Health check funcionando
- [ ] Documentação acessível
- [ ] Teste do endpoint `/gerar-match` funcionando
- [ ] Link de deploy adicionado no README

---

## 🧪 Testar o Deploy

Após o deploy, teste com:

```bash
# Health Check
curl https://sua-api.onrender.com/health

# Teste completo (use o script test_api.py modificado)
# Altere BASE_URL no test_api.py para sua URL de produção
```

Ou use o Postman/Insomnia para testar os endpoints.

---

## ⚠️ Observações Importantes

### Render.com (Free Tier)

- **Limitação**: Após 15 minutos de inatividade, o serviço "dorme"
- **Primeira requisição**: Pode demorar 30-60 segundos (wake up)
- **Solução**: Para produção, considere o plano pago ou use Railway

### Railway (Free Tier)

- Mais rápido que Render
- Não "dorme" como o Render
- Limite de uso mensal (geralmente suficiente para testes)

### Fly.io (Free Tier)

- Boa performance
- Requer configuração via CLI
- Mais técnico

---

## 🔗 Links Úteis

- **Render.com**: https://render.com
- **Railway**: https://railway.app
- **Fly.io**: https://fly.io
- **FastAPI Deploy Guide**: https://fastapi.tiangolo.com/deployment/

---

## 🆘 Troubleshooting

### Erro: "Module not found"
- Verifique se todas as dependências estão no `requirements.txt`
- Execute `pip freeze > requirements.txt` localmente para garantir

### Erro: "Port already in use"
- Render usa a variável `$PORT` automaticamente
- Certifique-se de usar `--port $PORT` no start command

### Erro: "GOOGLE_AI_KEY not found"
- Verifique se a variável de ambiente está configurada no Render
- Reinicie o serviço após adicionar variáveis

### Build falha
- Verifique os logs no Render
- Certifique-se de que o Python 3.8+ está sendo usado
- Verifique se não há erros de sintaxe no código

---

**Boa sorte com o deploy! 🚀**

