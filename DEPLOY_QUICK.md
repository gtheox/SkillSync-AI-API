# 🚀 Deploy Rápido - 5 Minutos

## Passo a Passo Simplificado

### 1. Preparar GitHub (2 min)

```bash
cd /Users/gabrielteodoro/GS/IA

# Se ainda não tem git inicializado
git init
git add .
git commit -m "Initial commit"

# Conectar ao GitHub (crie o repo primeiro em github.com)
git remote add origin https://github.com/SEU_USUARIO/skillsync-ai-api.git
git branch -M main
git push -u origin main
```

### 2. Deploy no Render.com (3 min)

1. **Acesse**: https://render.com
2. **Login** com GitHub
3. **New +** → **Web Service**
4. **Conecte** seu repositório
5. **Configure**:
   - **Name**: `skillsync-ai-api`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. **Environment Variables**:
   - Key: `GOOGLE_AI_KEY`
   - Value: `sua_chave_aqui`
7. **Create Web Service**

### 3. Pronto! ✅

Sua API estará em: `https://skillsync-ai-api.onrender.com`

Teste:
```bash
curl https://skillsync-ai-api.onrender.com/health
```

---

**📚 Para mais detalhes, veja [DEPLOY_TUTORIAL.md](./DEPLOY_TUTORIAL.md)**

