document.addEventListener('DOMContentLoaded', () => {
    const repoPathInput = document.getElementById('repoPath');
    const getFileTreeBtn = document.getElementById('getFileTree');
    const fileTreeDisplay = document.getElementById('fileTree');
    const promptInput = document.getElementById('prompt');
    const generatePlanBtn = document.getElementById('generatePlan');
    const planDisplay = document.getElementById('plan');
    const executePlanBtn = document.getElementById('executePlan');
    const resultDisplay = document.getElementById('result');
    
    // New Git-related elements
    const initRepoBtn = document.getElementById('initRepo');
    const repoStatusBtn = document.getElementById('repoStatus');
    const stageChangesBtn = document.getElementById('stageChanges');
    const commitChangesBtn = document.getElementById('commitChanges');
    const commitMessageInput = document.getElementById('commitMessage');
    const commitHistoryBtn = document.getElementById('commitHistory');
    const gitOperationsDisplay = document.getElementById('gitOperations');

    getFileTreeBtn.addEventListener('click', async () => {
        const repoPath = repoPathInput.value;
        if (!repoPath) {
            showError('Please enter a repository path.');
            return;
        }

        try {
            const response = await fetch('/get_file_tree', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ repoPath })
            });

            if (!response.ok) throw new Error('Failed to get file tree');

            const data = await response.json();
            fileTreeDisplay.textContent = JSON.stringify(data.fileTree, null, 2);
        } catch (error) {
            showError(error.message);
        }
    });

    generatePlanBtn.addEventListener('click', async () => {
        const repoPath = repoPathInput.value;
        const prompt = promptInput.value;
        if (!repoPath || !prompt) {
            showError('Please enter both repository path and prompt.');
            return;
        }

        try {
            const response = await fetch('/generate_plan', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ repoPath, prompt })
            });

            if (!response.ok) throw new Error('Failed to generate plan');

            const data = await response.json();
            planDisplay.textContent = data.plan;
        } catch (error) {
            showError(error.message);
        }
    });

    executePlanBtn.addEventListener('click', async () => {
        const repoPath = repoPathInput.value;
        const plan = planDisplay.textContent;
        if (!repoPath || !plan) {
            showError('Please generate a plan first.');
            return;
        }

        try {
            const response = await fetch('/execute_plan', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ repoPath, plan })
            });

            if (!response.ok) throw new Error('Failed to execute plan');

            const data = await response.json();
            resultDisplay.textContent = JSON.stringify(data.result, null, 2);
        } catch (error) {
            showError(error.message);
        }
    });

    // New Git-related event listeners
    initRepoBtn.addEventListener('click', async () => {
        const repoPath = repoPathInput.value;
        if (!repoPath) {
            showError('Please enter a repository path.');
            return;
        }

        try {
            const response = await fetch('/init_repo', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ repoPath })
            });

            if (!response.ok) throw new Error('Failed to initialize repository');

            const data = await response.json();
            gitOperationsDisplay.textContent = data.result;
        } catch (error) {
            showError(error.message);
        }
    });

    repoStatusBtn.addEventListener('click', async () => {
        const repoPath = repoPathInput.value;
        if (!repoPath) {
            showError('Please enter a repository path.');
            return;
        }

        try {
            const response = await fetch('/repo_status', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ repoPath })
            });

            if (!response.ok) throw new Error('Failed to get repository status');

            const data = await response.json();
            gitOperationsDisplay.textContent = data.status;
        } catch (error) {
            showError(error.message);
        }
    });

    stageChangesBtn.addEventListener('click', async () => {
        const repoPath = repoPathInput.value;
        if (!repoPath) {
            showError('Please enter a repository path.');
            return;
        }

        try {
            const response = await fetch('/stage_changes', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ repoPath })
            });

            if (!response.ok) throw new Error('Failed to stage changes');

            const data = await response.json();
            gitOperationsDisplay.textContent = data.result;
        } catch (error) {
            showError(error.message);
        }
    });

    commitChangesBtn.addEventListener('click', async () => {
        const repoPath = repoPathInput.value;
        const message = commitMessageInput.value;
        if (!repoPath || !message) {
            showError('Please enter both repository path and commit message.');
            return;
        }

        try {
            const response = await fetch('/commit_changes', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ repoPath, message })
            });

            if (!response.ok) throw new Error('Failed to commit changes');

            const data = await response.json();
            gitOperationsDisplay.textContent = data.result;
        } catch (error) {
            showError(error.message);
        }
    });

    commitHistoryBtn.addEventListener('click', async () => {
        const repoPath = repoPathInput.value;
        if (!repoPath) {
            showError('Please enter a repository path.');
            return;
        }

        try {
            const response = await fetch('/commit_history', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ repoPath })
            });

            if (!response.ok) throw new Error('Failed to get commit history');

            const data = await response.json();
            gitOperationsDisplay.textContent = JSON.stringify(data.history, null, 2);
        } catch (error) {
            showError(error.message);
        }
    });

    function showError(message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error';
        errorDiv.textContent = message;
        document.body.appendChild(errorDiv);
        setTimeout(() => errorDiv.remove(), 5000);
    }
});
