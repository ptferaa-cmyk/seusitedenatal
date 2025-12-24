# 🚀 GUIA RÁPIDO DE USO (ATUALIZADO)

Para facilitar o teste da aplicação, adicionei um formulário HTML simples que permite criar um site romântico sem precisar usar comandos `curl`.

## 🛠️ Como Testar Localmente (Passo a Passo)

### 1. Inicie o Servidor Flask
Certifique-se de que você está no diretório `romantic_site_generator` e que o ambiente virtual está ativado.

```bash
# Se não estiver no diretório:
cd romantic_site_generator

# Se o venv não estiver ativado:
source venv/bin/activate

# Inicie o servidor:
python3 app.py
```
O servidor estará rodando em `http://localhost:5001`.

### 2. Acesse o Formulário no Navegador
Abra o link abaixo no seu navegador. Ele agora aponta para o formulário de criação:

➡️ **http://localhost:5001/**

### 3. Crie o Site
1. **Preencha** os campos do formulário (nomes, data, mensagens, URLs das fotos).
2. **Clique** no botão "🚀 Criar Meu Site Romântico".
3. Uma mensagem de sucesso aparecerá com o **link final** do site.

### 4. Acesse o Site Criado
Clique no link retornado (ex: `http://localhost:5001/site/beatriz-carlos-5ad09c`) para ver o site romântico funcionando perfeitamente!

---

## 📦 Arquivos Incluídos (Atualizados)

O arquivo ZIP final foi atualizado e contém:

- **`romantic_site_generator/static/formulario.html`**: O novo formulário HTML.
- **`romantic_site_generator/app.py`**: Atualizado para servir o formulário na rota `/`.
- **`romantic_site_generator/teste_automatico.sh`**: Script de teste automatizado (ainda funcional).
- **`romantic_site_generator/screenshot_formulario_sucesso.webp`**: Prova visual do formulário e da mensagem de sucesso.
- **`romantic_site_generator/screenshot_site_funcionando.webp`**: Prova visual do site criado.

---

## ✅ Prova Visual do Formulário Funcionando

O formulário permite que você crie o site de forma visual, eliminando a necessidade de usar o `curl`.

![Screenshot do Formulário de Criação](screenshot_formulario_sucesso.webp)

Ao clicar no link retornado, você verá o site funcionando perfeitamente, como na imagem abaixo:

![Screenshot do Site Criado](screenshot_site_funcionando.webp)

