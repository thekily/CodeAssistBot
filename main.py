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
        logger.info(f"Received prompt: {prompt}")
        if not prompt:
            return jsonify({'error': 'No prompt provided'}), 400

        file_tree = get_file_tree(app.config['UPLOAD_FOLDER'])
        logger.info(f"File tree for plan generation: {file_tree}")
        plan = generate_plan(prompt, file_tree)
        logger.info(f"Generated plan: {plan}")
        return jsonify({'plan': plan}), 200
    except Exception as e:
        logger.error(f"Error generating plan: {e}")
        return jsonify({'error': f'An error occurred while generating the plan: {str(e)}'}), 500

@app.route('/execute_plan', methods=['POST'])
def execute_plan_route():
    try:
        data = request.json
        plan = data.get('plan')
        if not plan:
            return jsonify({'error': 'No plan provided'}), 400

        result = execute_plan(plan, app.config['UPLOAD_FOLDER'])
        return jsonify({'result': result})
    except Exception as e:
        logger.error(f"Error executing plan: {e}")
        return jsonify({'error': f'An error occurred while executing the plan: {str(e)}'}), 500

@app.route('/git_init', methods=['POST'])
def git_init_route():
    try:
        result = initialize_git_repo(app.config['UPLOAD_FOLDER'])
        return jsonify({'result': result})
    except Exception as e:
        logger.error(f"Error initializing Git repository: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/git_add', methods=['POST'])
def git_add_route():
    try:
        result = git_add_all(app.config['UPLOAD_FOLDER'])
        return jsonify({'result': result})
    except Exception as e:
        logger.error(f"Error staging changes: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/git_commit', methods=['POST'])
def git_commit_route():
    try:
        data = request.json
        message = data.get('message')
        if not message:
            return jsonify({'error': 'No commit message provided'}), 400
        result = git_commit(app.config['UPLOAD_FOLDER'], message)
        return jsonify({'result': result})
    except Exception as e:
        logger.error(f"Error committing changes: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/git_status', methods=['POST'])
def git_status_route():
    try:
        result = git_status(app.config['UPLOAD_FOLDER'])
        return jsonify({'result': result})
    except Exception as e:
        logger.error(f"Error getting Git status: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
