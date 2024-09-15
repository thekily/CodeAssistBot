import os
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from utils.file_operations import get_file_tree, read_file_content, write_file_content
from utils.openai_integration import generate_plan, execute_plan
from utils.git_operations import initialize_git_repo, git_add_all, git_commit, git_status
import logging
import tempfile

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

UPLOAD_FOLDER = tempfile.mkdtemp()
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_files', methods=['POST'])
def upload_files():
    if 'files' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    files = request.files.getlist('files')
    if not files:
        return jsonify({'error': 'No selected file'}), 400
    
    try:
        total_files = len(files)
        for i, file in enumerate(files, 1):
            if file:
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                file.save(file_path)
        
        file_tree = get_file_tree(app.config['UPLOAD_FOLDER'])
        if not file_tree:
            raise Exception("Failed to generate file tree")
        
        logger.info(f"File tree generated: {file_tree}")
        return jsonify({'fileTree': file_tree})
    except Exception as e:
        logger.error(f"Error uploading files: {e}")
        return jsonify({'error': f'An error occurred while uploading files: {str(e)}'}), 500

@app.route('/generate_plan', methods=['POST'])
def generate_plan_route():
    try:
        data = request.json
        prompt = data.get('prompt')
        if not prompt:
            return jsonify({'error': 'No prompt provided'}), 400

        file_tree = get_file_tree(app.config['UPLOAD_FOLDER'])
        plan = generate_plan(prompt, file_tree)
        return jsonify({'plan': plan})
    except Exception as e:
        logger.error(f"Error generating plan: {e}")
        return jsonify({'error': f'An error occurred while generating the plan: {str(e)}'}), 500

# ... (rest of the code remains unchanged)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
