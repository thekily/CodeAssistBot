import os
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from utils.file_operations import get_file_tree, read_file_content, write_file_content
from utils.openai_integration import generate_plan, execute_plan
from utils.git_operations import initialize_git_repo, git_add_all, git_commit, git_status
import logging
import tempfile
import shutil

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
        for file in files:
            if file:
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        file_tree = get_file_tree(app.config['UPLOAD_FOLDER'])
        return jsonify({'fileTree': file_tree})
    except Exception as e:
        logger.error(f"Error uploading files: {e}")
        return jsonify({'error': 'An error occurred while uploading files'}), 500

@app.route('/generate_plan', methods=['POST'])
def generate_plan_route():
    prompt = request.json.get('prompt')
    if not prompt:
        return jsonify({'error': 'Prompt not provided'}), 400
    try:
        file_tree = get_file_tree(app.config['UPLOAD_FOLDER'])
        plan = generate_plan(prompt, file_tree)
        return jsonify({'plan': plan})
    except Exception as e:
        logger.error(f"Error in generate_plan: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/execute_plan', methods=['POST'])
def execute_plan_route():
    plan = request.json.get('plan')
    if not plan:
        return jsonify({'error': 'Plan not provided'}), 400
    try:
        result = execute_plan(plan, app.config['UPLOAD_FOLDER'])
        return jsonify({'result': result})
    except Exception as e:
        logger.error(f"Error in execute_plan: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/git_init', methods=['POST'])
def git_init_route():
    try:
        result = initialize_git_repo(app.config['UPLOAD_FOLDER'])
        return jsonify({'result': result})
    except Exception as e:
        logger.error(f"Error in git_init: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/git_add', methods=['POST'])
def git_add_route():
    try:
        result = git_add_all(app.config['UPLOAD_FOLDER'])
        return jsonify({'result': result})
    except Exception as e:
        logger.error(f"Error in git_add: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/git_commit', methods=['POST'])
def git_commit_route():
    message = request.json.get('message')
    if not message:
        return jsonify({'error': 'Commit message not provided'}), 400
    try:
        result = git_commit(app.config['UPLOAD_FOLDER'], message)
        return jsonify({'result': result})
    except Exception as e:
        logger.error(f"Error in git_commit: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/git_status', methods=['POST'])
def git_status_route():
    try:
        result = git_status(app.config['UPLOAD_FOLDER'])
        return jsonify({'result': result})
    except Exception as e:
        logger.error(f"Error in git_status: {e}")
        return jsonify({'error': str(e)}), 500

@app.teardown_appcontext
def cleanup(error):
    shutil.rmtree(app.config['UPLOAD_FOLDER'], ignore_errors=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
