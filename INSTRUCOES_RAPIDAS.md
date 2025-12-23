# 🚀 Guia Rápido - Gerador de Sites Românticos

## ⚡ Início Rápido (3 passos)

### 1️⃣ Instalar Dependências
```bash
cd romantic_site_generator
python3 -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2️⃣ Iniciar o Servidor
```bash
python3 app.py
```
✅ Servidor rodando em: `http://localhost:5001`

### 3️⃣ Criar um Site
```bash
curl -X POST http://localhost:5001/criar-site \
  -H "Content-Type: application/json" \
  -d '{
    "nome_homenageada": "Maria",
    "nome_presenteador": "João",
    "data_inicio_relacionamento": "2020-02-14",
    "mensagem_principal": "Você é incrível!",
    "fotos": [
      "https://images.pexels.com/photos/1024993/pexels-photo-1024993.jpeg",
      "https://images.pexels.com/photos/1024998/pexels-photo-1024998.jpeg",
      "https://images.pexels.com/photos/1024992/pexels-photo-1024992.jpeg"
    ]
  }'
```

## 📋 Campos da API

### ✅ Obrigatórios
- `nome_homenageada` - Nome da pessoa homenageada
- `nome_presenteador` - Nome de quem presenteia
- `data_inicio_relacionamento` - Formato: YYYY-MM-DD
- `mensagem_principal` - Mensagem romântica
- `fotos` - Array com 3 a 8 URLs de imagens

### 🎨 Opcionais
- `musica` - URL do YouTube ou MP3
- `momentos` - Array de objetos: `{"data": "YYYY-MM-DD", "descricao_curta": "texto"}`
- `mensagem_final` - Mensagem de encerramento

## 🎯 Exemplo Completo

```json
{
  "nome_homenageada": "Beatriz",
  "nome_presenteador": "Carlos",
  "data_inicio_relacionamento": "2018-12-25",
  "mensagem_principal": "Você é meu presente de Natal todos os dias!",
  "fotos": [
    "https://images.pexels.com/photos/1024993/pexels-photo-1024993.jpeg",
    "https://images.pexels.com/photos/1024998/pexels-photo-1024998.jpeg",
    "https://images.pexels.com/photos/1024992/pexels-photo-1024992.jpeg",
    "https://images.pexels.com/photos/1024997/pexels-photo-1024997.jpeg"
  ],
  "musica": "https://www.youtube.com/watch?v=CmDj_dV1n-A",
  "momentos": [
    {
      "data": "2018-12-25",
      "descricao_curta": "Nosso primeiro Natal juntos"
    },
    {
      "data": "2020-02-14",
      "descricao_curta": "Dia dos Namorados inesquecível"
    }
  ],
  "mensagem_final": "Te amo para sempre!"
}
```

## 📱 Funcionalidades do Site Gerado

✨ **Título personalizado** com nomes e emoji de coração
📸 **Carrossel de fotos** com navegação e autoplay
⏱️ **Contador de tempo** (anos, meses, dias)
💌 **Mensagem romântica** em formato de carta
🎯 **Momentos marcantes** em cards elegantes
🎵 **Player de música** (YouTube ou MP3)
💝 **Mensagem final** com destaque especial
📱 **Design responsivo** para mobile e desktop

## 🎨 URLs de Imagens de Exemplo

Use estas URLs gratuitas do Pexels para testar:

```
https://images.pexels.com/photos/1024993/pexels-photo-1024993.jpeg
https://images.pexels.com/photos/1024998/pexels-photo-1024998.jpeg
https://images.pexels.com/photos/1024992/pexels-photo-1024992.jpeg
https://images.pexels.com/photos/1024997/pexels-photo-1024997.jpeg
https://images.pexels.com/photos/1024995/pexels-photo-1024995.jpeg
```

## 🔗 Endpoints da API

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/criar-site` | Cria um novo site |
| GET | `/api/site/<slug>` | Retorna dados do site (JSON) |
| GET | `/site/<slug>` | Exibe o site no navegador |

## 💡 Dicas

1. **Fotos:** Use URLs públicas e acessíveis
2. **Datas:** Sempre no formato YYYY-MM-DD
3. **Música:** YouTube ou link direto para MP3
4. **Slug:** Gerado automaticamente e único
5. **Dados:** Salvos em `sites_data.json`

## 🆘 Problemas Comuns

**Erro: "Campo obrigatório ausente"**
→ Verifique se todos os campos obrigatórios estão presentes

**Erro: "fotos deve ser um array com 3 a 8 URLs"**
→ Envie entre 3 e 8 URLs de fotos

**Site não carrega**
→ Verifique se o servidor está rodando e se o slug está correto

## 📚 Documentação Completa

Consulte o arquivo `README.md` para documentação detalhada.

---

**Desenvolvido com ❤️ seguindo os requisitos dos prompts fornecidos**

