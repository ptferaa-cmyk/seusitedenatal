# Gerador de Sites Românticos Personalizados

## Descrição

Este é um produto digital que gera automaticamente sites românticos personalizados. O sistema permite que usuários criem páginas únicas e emocionais para homenagear pessoas especiais, com fotos, mensagens, contador de tempo juntos, momentos marcantes e música de fundo.

## Tecnologias Utilizadas

### Backend
- **Python 3.11**
- **Flask 3.0.0** - Framework web
- **Flask-CORS 4.0.0** - Suporte a requisições cross-origin
- **JSON** - Armazenamento de dados

### Frontend
- **HTML5**
- **CSS3** - Design responsivo e animações
- **JavaScript (Vanilla)** - Interatividade e consumo de API

## Estrutura do Projeto

```
romantic_site_generator/
├── app.py                  # Arquivo principal do backend (desenvolvimento)
├── src/
│   └── main.py            # Arquivo principal para deploy
├── static/
│   ├── index.html         # Página principal do site gerado
│   ├── style.css          # Estilos do site
│   └── script.js          # Lógica do frontend
├── requirements.txt       # Dependências Python
├── sites_data.json        # Banco de dados (gerado automaticamente)
└── venv/                  # Ambiente virtual Python
```

## Instalação e Configuração

### 1. Clonar ou baixar o projeto

```bash
cd romantic_site_generator
```

### 2. Criar ambiente virtual

```bash
python3 -m venv venv
```

### 3. Ativar o ambiente virtual

**Linux/Mac:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

### 4. Instalar dependências

```bash
pip install -r requirements.txt
```

## Como Usar

### Iniciar o servidor

```bash
python3 app.py
```

O servidor estará disponível em: `http://localhost:5001`

### Criar um novo site

Faça uma requisição POST para `/criar-site` com os dados do site:

```bash
curl -X POST http://localhost:5001/criar-site \
  -H "Content-Type: application/json" \
  -d '{
    "nome_homenageada": "Maria",
    "nome_presenteador": "João",
    "data_inicio_relacionamento": "2020-02-14",
    "mensagem_principal": "Você é a pessoa mais incrível que já conheci!",
    "fotos": [
      "https://exemplo.com/foto1.jpg",
      "https://exemplo.com/foto2.jpg",
      "https://exemplo.com/foto3.jpg"
    ],
    "musica": "https://www.youtube.com/watch?v=exemplo",
    "momentos": [
      {
        "data": "2020-02-14",
        "descricao_curta": "Nosso primeiro encontro"
      }
    ],
    "mensagem_final": "Te amo para sempre!"
  }'
```

### Resposta da API

```json
{
  "success": true,
  "slug": "maria-joao-a81fd7",
  "link_final_do_site": "http://localhost:5001/site/maria-joao-a81fd7"
}
```

### Acessar o site gerado

Abra o navegador e acesse o link retornado pela API.

## Documentação da API

### POST /criar-site

Cria um novo site romântico personalizado.

**Campos Obrigatórios:**
- `nome_homenageada` (string) - Nome da pessoa homenageada
- `nome_presenteador` (string) - Nome de quem está presenteando
- `data_inicio_relacionamento` (string) - Data no formato YYYY-MM-DD
- `mensagem_principal` (string) - Mensagem romântica principal
- `fotos` (array) - Array com 3 a 8 URLs de fotos

**Campos Opcionais:**
- `musica` (string) - URL do YouTube ou link MP3
- `momentos` (array) - Array de objetos com `data` e `descricao_curta`
- `mensagem_final` (string) - Mensagem final de impacto

**Resposta de Sucesso (201):**
```json
{
  "success": true,
  "slug": "nome-slug-gerado",
  "link_final_do_site": "http://localhost:5001/site/nome-slug-gerado"
}
```

**Resposta de Erro (400):**
```json
{
  "success": false,
  "error": "Descrição do erro"
}
```

### GET /api/site/<slug>

Retorna os dados de um site específico.

**Parâmetros:**
- `slug` (string) - Identificador único do site

**Resposta de Sucesso (200):**
```json
{
  "slug": "maria-joao-a81fd7",
  "nome_homenageada": "Maria",
  "nome_presenteador": "João",
  "data_inicio_relacionamento": "2020-02-14",
  "mensagem_principal": "Você é a pessoa mais incrível...",
  "fotos": ["url1", "url2", "url3"],
  "musica": "https://youtube.com/...",
  "momentos": [...],
  "mensagem_final": "Te amo para sempre!",
  "created_at": "2025-12-22T18:40:23.939257"
}
```

**Resposta de Erro (404):**
```json
{
  "success": false,
  "error": "Site não encontrado"
}
```

### GET /site/<slug>

Exibe o site romântico personalizado no navegador.

**Parâmetros:**
- `slug` (string) - Identificador único do site

## Funcionalidades do Frontend

### 1. Título Personalizado
Exibe "Para {nome_homenageada}, com amor — {nome_presenteador} 💖"

### 2. Carrossel de Imagens
- Navegação por botões (anterior/próximo)
- Indicadores de posição
- Autoplay a cada 5 segundos
- Suporte a swipe no mobile

### 3. Contador de Tempo Juntos
Calcula automaticamente anos, meses e dias desde o início do relacionamento.

### 4. Mensagem Romântica
Exibida em formato de carta elegante com assinatura.

### 5. Momentos que Marcaram
Renderiza cards com datas formatadas e descrições dos momentos especiais.

### 6. Mensagem Final
Destaque visual para a mensagem final de impacto.

### 7. Player de Música
- Botão play/pause para arquivos MP3
- Link para vídeo do YouTube
- Posicionado no canto inferior direito

### 8. Design Responsivo
- Mobile-first
- Animações suaves (fade-in, slide)
- Efeitos hover
- Compatível com todos os dispositivos

## Exemplo Completo de Uso

```python
import requests
import json

# URL da API
api_url = "http://localhost:5001/criar-site"

# Dados do site
dados = {
    "nome_homenageada": "Beatriz",
    "nome_presenteador": "Carlos",
    "data_inicio_relacionamento": "2018-12-25",
    "mensagem_principal": "Você é meu presente de Natal todos os dias do ano. Te amo infinitamente!",
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
        },
        {
            "data": "2022-07-15",
            "descricao_curta": "Viagem dos sonhos para Paris"
        }
    ],
    "mensagem_final": "Que nossa história continue sendo escrita com muito amor e cumplicidade!"
}

# Criar o site
response = requests.post(api_url, json=dados)
resultado = response.json()

print(f"Site criado com sucesso!")
print(f"Link: {resultado['link_final_do_site']}")
print(f"Slug: {resultado['slug']}")
```

## Cores e Estilo

O site utiliza um gradiente roxo/azul elegante:
- **Fundo principal:** Gradiente de #667eea para #764ba2
- **Texto:** Branco e tons de cinza
- **Destaques:** Rosa (#ff4f81)
- **Fonte:** Georgia (serif) para elegância

## Observações Importantes

1. **Armazenamento:** Os dados são salvos em `sites_data.json` no mesmo diretório do aplicativo
2. **Slugs:** São gerados automaticamente e são únicos para cada site
3. **Fotos:** Devem ser URLs públicas e acessíveis
4. **Música:** Suporta URLs do YouTube ou links diretos para arquivos MP3
5. **Datas:** Devem estar no formato YYYY-MM-DD

## Melhorias Futuras

- Banco de dados SQL para melhor escalabilidade
- Upload de imagens direto no servidor
- Temas personalizáveis
- Exportação para PDF
- Sistema de autenticação
- Painel administrativo
- Análise de visualizações

## Suporte

Para dúvidas ou problemas, entre em contato através do repositório do projeto.

## Licença

Este projeto foi desenvolvido como um produto digital personalizado.

