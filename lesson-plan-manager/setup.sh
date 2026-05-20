#!/bin/bash
# ─────────────────────────────────────────────────────────────
#  PlanEduca — Script de configuração inicial
#  Uso: bash setup.sh
# ─────────────────────────────────────────────────────────────

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo ""
echo "╔══════════════════════════════════════╗"
echo "║   PlanEduca — Setup Inicial          ║"
echo "╚══════════════════════════════════════╝"
echo ""

# 1. Verificar dependências
echo "🔍 Verificando dependências..."

if ! command -v docker &> /dev/null; then
  echo -e "${RED}✗ Docker não encontrado. Instale em: https://docs.docker.com/get-docker/${NC}"
  exit 1
fi
echo -e "${GREEN}✓ Docker OK${NC}"

if ! command -v docker compose &> /dev/null && ! docker-compose version &> /dev/null 2>&1; then
  echo -e "${RED}✗ Docker Compose não encontrado.${NC}"
  exit 1
fi
echo -e "${GREEN}✓ Docker Compose OK${NC}"

# 2. Criar .env se não existir
if [ ! -f backend/.env ]; then
  echo ""
  echo "📋 Criando backend/.env a partir do .env.example..."
  cp backend/.env.example backend/.env
  echo -e "${YELLOW}⚠️  IMPORTANTE: Adicione sua ANTHROPIC_API_KEY no arquivo backend/.env${NC}"
  echo ""

  # Tenta abrir o editor automaticamente
  if command -v nano &> /dev/null; then
    read -p "   Deseja abrir o arquivo agora para editar? (s/N): " OPEN_EDITOR
    if [[ "$OPEN_EDITOR" =~ ^[Ss]$ ]]; then
      nano backend/.env
    fi
  else
    echo "   Edite manualmente: nano backend/.env  ou  code backend/.env"
  fi
else
  echo -e "${GREEN}✓ backend/.env já existe${NC}"
fi

# 3. Verificar se a chave foi configurada
if grep -q "your_anthropic_api_key_here" backend/.env; then
  echo ""
  echo -e "${RED}✗ ANTHROPIC_API_KEY ainda não foi configurada em backend/.env${NC}"
  echo "   Edite o arquivo e substitua 'your_anthropic_api_key_here' pela sua chave."
  echo "   Obtenha em: https://console.anthropic.com"
  echo ""
  echo "   Depois rode novamente: bash setup.sh"
  exit 1
fi

echo -e "${GREEN}✓ ANTHROPIC_API_KEY configurada${NC}"

# 4. Subir a aplicação
echo ""
echo "🐳 Construindo e iniciando os containers..."
echo "   (Primeira vez pode demorar 2-3 minutos)"
echo ""

docker compose up --build -d

# 5. Aguardar o backend ficar saudável
echo ""
echo "⏳ Aguardando o backend inicializar..."
ATTEMPTS=0
MAX=20
until curl -sf http://localhost:3000/health > /dev/null 2>&1; do
  ATTEMPTS=$((ATTEMPTS+1))
  if [ $ATTEMPTS -ge $MAX ]; then
    echo -e "${RED}✗ Backend não respondeu após ${MAX} tentativas.${NC}"
    echo "   Verifique os logs: docker compose logs backend"
    exit 1
  fi
  sleep 3
  echo -n "."
done

echo ""
echo ""
echo "╔══════════════════════════════════════════╗"
echo "║  ✅  PlanEduca está rodando!             ║"
echo "║                                          ║"
echo "║  🌐  http://localhost:3000               ║"
echo "║  🏥  http://localhost:3000/health        ║"
echo "║  📋  Logs: docker compose logs -f        ║"
echo "╚══════════════════════════════════════════╝"
echo ""
