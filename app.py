from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from datetime import datetime
import hashlib
import re
import requests
from werkzeug.utils import secure_filename
from urllib.parse import urljoin

# --- Configurações Supabase (Fornecidas pelo Usuário) ---
SUPABASE_URL = "https://kxiqujsxnncyfcjblspy.supabase.co"
SUPABASE_SERVICE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imt4aXF1anN4bm5jeWZjamJsc3B5Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NjQ0OTIyMSwiZXhwIjoyMDgyMDI1MjIxfQ.5TKcpLKJ7UMSDOHnyql86YAEjQYiDakDA6KBdrwEPFU"
SUPABASE_BUCKET = "fotos-sites"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
MAX_FILE_SIZE = 5 * 1024 * 1024 # 5MB

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, 'static')

app = Flask(__name__, static_folder=STATIC_DIR)
CORS(app)

DATA_FILE = 'sites_data.json'

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def generate_slug(nome_homenageada, nome_presenteador):
    base = f"{nome_homenageada}-{nome_presenteador}".lower()
    base = re.sub(r'[^a-z0-9]+', '-', base)
    base = base.strip('-')
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    hash_part = hashlib.md5(timestamp.encode()).hexdigest()[:6]
    return f"{base}-{hash_part}"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_to_supabase(file, slug):
    """Faz o upload de um arquivo para o Supabase Storage e retorna a URL pública."""
    
    filename = secure_filename(file.filename)
    file_extension = filename.rsplit('.', 1)[1].lower()
    
    # Gera um nome de arquivo único
    unique_filename = f"{slug}/{hashlib.sha256(os.urandom(64)).hexdigest()}.{file_extension}"
    
    upload_url = urljoin(SUPABASE_URL, f"/storage/v1/object/{SUPABASE_BUCKET}/{unique_filename}")
    
    headers = {
        "Authorization": f"Bearer {SUPABASE_SERVICE_KEY}",
        "Content-Type": file.content_type,
        "x-upsert": "true" # Sobrescreve se existir
    }
    
    # Volta o ponteiro do arquivo para o início antes de ler o conteúdo
    file.seek(0)
    
    try:
        response = requests.post(upload_url, headers=headers, data=file.read())
        response.raise_for_status() # Levanta exceção para códigos de erro HTTP
        
        # A URL pública é construída manualmente, pois a API de upload retorna apenas o path
        public_url = urljoin(SUPABASE_URL, f"/storage/v1/object/public/{SUPABASE_BUCKET}/{unique_filename}")
        return public_url
        
    except requests.exceptions.RequestException as e:
        app.logger.error(f"Erro ao fazer upload para Supabase: {e}")
        return None

@app.route('/', methods=['GET'])
def home():
    return app.send_static_file('formulario.html')

@app.route('/criar-site', methods=['POST'])
def criar_site():
    
    # 1. Coleta e validação dos dados de texto
    data = request.form
    
    required_fields = ['nome_homenageada', 'nome_presenteador', 'data_inicio_relacionamento', 'mensagem_principal']
    
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({'success': False, 'error': f'Campo obrigatório ausente: {field}'}), 400

    # 2. Coleta e validação das fotos
    if 'fotos' not in request.files:
        return jsonify({'success': False, 'error': 'Nenhuma foto enviada'}), 400
    
    uploaded_files = request.files.getlist('fotos')
    
    if len(uploaded_files) < 3 or len(uploaded_files) > 8:
        return jsonify({'success': False, 'error': f'O número de fotos deve ser entre 3 e 8. Enviado: {len(uploaded_files)}'}), 400
    
    # 3. Processamento e Upload das Fotos
    fotos_urls = []
    slug = generate_slug(data['nome_homenageada'], data['nome_presenteador'])
    
    for file in uploaded_files:
        if file.filename == '':
            continue
        
        if not allowed_file(file.filename):
            return jsonify({'success': False, 'error': f'Tipo de arquivo não permitido: {file.filename}'}), 400
        
        # Verifica o tamanho do arquivo (limitação básica, o Supabase fará a validação final)
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        if file_size > MAX_FILE_SIZE:
            return jsonify({'success': False, 'error': f'O arquivo {file.filename} excede o tamanho máximo de 5MB.'}), 400
        
        # Faz o upload
        public_url = upload_to_supabase(file, slug)
        
        if public_url is None:
            return jsonify({'success': False, 'error': f'Falha ao fazer upload da foto {file.filename} para o Supabase.'}), 500
            
        fotos_urls.append(public_url)

    # 4. Processamento de Momentos (que vem como JSON string no FormData)
    momentos_raw = data.get('momentos')
    momentos = []
    if momentos_raw:
        try:
            momentos = json.loads(momentos_raw)
        except json.JSONDecodeError:
            return jsonify({'success': False, 'error': 'Formato inválido para Momentos.'}), 400

    # 5. Criação e Salvamento dos Dados do Site
    site_data = {
        'slug': slug,
        'nome_homenageada': data['nome_homenageada'],
        'nome_presenteador': data['nome_presenteador'],
        'data_inicio_relacionamento': data['data_inicio_relacionamento'],
        'mensagem_principal': data['mensagem_principal'],
        'fotos': fotos_urls, # URLs públicas do Supabase
        'musica': data.get('musica', ''),
        'momentos': momentos,
        'mensagem_final': data.get('mensagem_final', ''),
        'created_at': datetime.now().isoformat()
    }
    
    all_data = load_data()
    all_data[slug] = site_data
    save_data(all_data)
    
    base_url = request.host_url.rstrip('/')
    link_final = f"{base_url}/site/{slug}"
    
    return jsonify({
        'success': True,
        'slug': slug,
        'link_final_do_site': link_final
    }), 201

@app.route('/api/site/<slug>', methods=['GET'])
def get_site(slug):
    all_data = load_data()
    
    if slug not in all_data:
        return jsonify({'success': False, 'error': 'Site não encontrado'}), 404
    
    return jsonify(all_data[slug]), 200

@app.route('/site/<slug>', methods=['GET'])
def view_site(slug):
    # Mantendo a referência ao index_novo.html, se for o front-end romântico
    return app.send_static_file('index_novo.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
