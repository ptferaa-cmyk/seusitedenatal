#!/bin/bash

echo "=========================================="
echo "🚀 TESTE AUTOMÁTICO - GERADOR DE SITES ROMÂNTICOS"
echo "=========================================="
echo ""

# Verificar se o servidor está rodando
echo "📡 Verificando se o servidor está rodando..."
if curl -s http://localhost:5001/criar-site > /dev/null 2>&1; then
    echo "✅ Servidor está rodando!"
else
    echo "❌ Servidor NÃO está rodando!"
    echo ""
    echo "Por favor, inicie o servidor primeiro:"
    echo "  python3 app.py"
    echo ""
    exit 1
fi

echo ""
echo "=========================================="
echo "📝 TESTE 1: Criando um site de teste..."
echo "=========================================="

# Criar um site de teste
RESPONSE=$(curl -s -X POST http://localhost:5001/criar-site \
  -H "Content-Type: application/json" \
  -d '{
    "nome_homenageada": "Maria",
    "nome_presenteador": "João",
    "data_inicio_relacionamento": "2020-02-14",
    "mensagem_principal": "Você é a pessoa mais incrível que já conheci. Cada dia ao seu lado é uma bênção e um presente. Te amo infinitamente!",
    "fotos": [
      "https://images.pexels.com/photos/1024993/pexels-photo-1024993.jpeg",
      "https://images.pexels.com/photos/1024998/pexels-photo-1024998.jpeg",
      "https://images.pexels.com/photos/1024992/pexels-photo-1024992.jpeg"
    ],
    "musica": "https://www.youtube.com/watch?v=CmDj_dV1n-A",
    "momentos": [
      {
        "data": "2020-02-14",
        "descricao_curta": "Nosso primeiro encontro, onde tudo começou"
      },
      {
        "data": "2021-06-20",
        "descricao_curta": "A viagem inesquecível para a praia"
      }
    ],
    "mensagem_final": "Obrigado por fazer parte da minha vida. Você é meu tudo!"
  }')

echo ""
echo "📋 Resposta da API:"
echo "$RESPONSE" | python3 -m json.tool

# Extrair o slug e o link
SLUG=$(echo "$RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin).get('slug', ''))")
LINK=$(echo "$RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin).get('link_final_do_site', ''))")

if [ -z "$SLUG" ]; then
    echo ""
    echo "❌ Erro ao criar o site!"
    exit 1
fi

echo ""
echo "✅ Site criado com sucesso!"
echo "   Slug: $SLUG"
echo "   Link: $LINK"

echo ""
echo "=========================================="
echo "📝 TESTE 2: Consultando dados do site via API..."
echo "=========================================="

API_DATA=$(curl -s "http://localhost:5001/api/site/$SLUG")
echo ""
echo "📋 Dados retornados pela API:"
echo "$API_DATA" | python3 -m json.tool

echo ""
echo "=========================================="
echo "📝 TESTE 3: Verificando se o site HTML está acessível..."
echo "=========================================="

HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost:5001/site/$SLUG")

if [ "$HTTP_STATUS" = "200" ]; then
    echo "✅ Site HTML está acessível! (HTTP $HTTP_STATUS)"
else
    echo "❌ Erro ao acessar o site HTML! (HTTP $HTTP_STATUS)"
fi

echo ""
echo "=========================================="
echo "🎉 TESTES CONCLUÍDOS!"
echo "=========================================="
echo ""
echo "🌐 Para visualizar o site no navegador, acesse:"
echo "   $LINK"
echo ""
echo "💡 Dica: Copie e cole o link acima no seu navegador!"
echo ""

