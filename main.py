import os
from flask import Flask, render_template, request, jsonify
from utils.file_operations import get_file_tree, read_file_content, write_file_content
from utils.openai_integration import generate_plan, execute_plan
from utils.git_operations import initialize_repo, get_repo_status, stage_changes, commit_changes, get_commit_history

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_file_tree', methods=['POST'])
def get_file_tree_route():
    repo_path = request.json.get('repoPath')
    if not repo_path:
        return jsonify({'error': 'Repository path not provided'}), 400
    try:
        file_tree = get_file_tree(repo_path)
        return jsonify({'fileTree': file_tree})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/generate_plan', methods=['POST'])
def generate_plan_route():
    prompt = request.json.get('prompt')
    repo_path = request.json.get('repoPath')
    if not prompt or not repo_path:
        return jsonify({'error': 'Prompt or repository path not provided'}), 400
    try:
        file_tree = get_file_tree(repo_path)
        plan = generate_plan(prompt, file_tree)
        return jsonify({'plan': plan})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/execute_plan', methods=['POST'])
def execute_plan_route():
    plan = request.json.get('plan')
    repo_path = request.json.get('repoPath')
    if not plan or not repo_path:
        return jsonify({'error': 'Plan or repository path not provided'}), 400
    try:
        result = execute_plan(plan, repo_path)
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/read_file', methods=['POST'])
def read_file_route():
    file_path = request.json.get('filePath')
    if not file_path:
        return jsonify({'error': 'File path not provided'}), 400
    try:
        content = read_file_content(file_path)
        return jsonify({'content': content})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/write_file', methods=['POST'])
def write_file_route():
    file_path = request.json.get('filePath')
    content = request.json.get('content')
    if not file_path or content is None:
        return jsonify({'error': 'File path or content not provided'}), 400
    try:
        write_file_content(file_path, content)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# New Git-related routes
@app.route('/init_repo', methods=['POST'])
def init_repo_route():
    repo_path = request.json.get('repoPath')
    if not repo_path:
        return jsonify({'error': 'Repository path not provided'}), 400
    try:
        result = initialize_repo(repo_path)
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/repo_status', methods=['POST'])
def repo_status_route():
    repo_path = request.json.get('repoPath')
    if not repo_path:
        return jsonify({'error': 'Repository path not provided'}), 400
    try:
        status = get_repo_status(repo_path)
        return jsonify({'status': status})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/stage_changes', methods=['POST'])
def stage_changes_route():
    repo_path = request.json.get('repoPath')
    file_path = request.json.get('filePath')
    if not repo_path:
        return jsonify({'error': 'Repository path not provided'}), 400
    try:
        result = stage_changes(repo_path, file_path)
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/commit_changes', methods=['POST'])
def commit_changes_route():
    repo_path = request.json.get('repoPath')
    message = request.json.get('message')
    if not repo_path or not message:
        return jsonify({'error': 'Repository path or commit message not provided'}), 400
    try:
        result = commit_changes(repo_path, message)
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/commit_history', methods=['POST'])
def commit_history_route():
    repo_path = request.json.get('repoPath')
    if not repo_path:
        return jsonify({'error': 'Repository path not provided'}), 400
    try:
        history = get_commit_history(repo_path)
        return jsonify({'history': history})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
