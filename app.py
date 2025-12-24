from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os
from datetime import datetime
import hashlib
import re

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

@app.route('/', methods=['GET'])
def home():
    return app.send_static_file('formulario.html')

@app.route('/criar-site', methods=['POST'])
def criar_site():
    data = request.get_json()
    
    required_fields = ['nome_homenageada', 'nome_presenteador', 'data_inicio_relacionamento', 'mensagem_principal', 'fotos']
    
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({'success': False, 'error': f'Campo obrigatório ausente: {field}'}), 400
    
    if not isinstance(data['fotos'], list) or len(data['fotos']) < 3 or len(data['fotos']) > 8:
        return jsonify({'success': False, 'error': 'fotos deve ser um array com 3 a 8 URLs'}), 400
    
    slug = generate_slug(data['nome_homenageada'], data['nome_presenteador'])
    
    site_data = {
        'slug': slug,
        'nome_homenageada': data['nome_homenageada'],
        'nome_presenteador': data['nome_presenteador'],
        'data_inicio_relacionamento': data['data_inicio_relacionamento'],
        'mensagem_principal': data['mensagem_principal'],
        'fotos': data['fotos'],
        'musica': data.get('musica', ''),
        'momentos': data.get('momentos', []),
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
    return app.send_static_file('index_novo.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)

