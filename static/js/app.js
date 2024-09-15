document.addEventListener('DOMContentLoaded', () => {
    const repoPathInput = document.getElementById('repoPath');
    const getFileTreeBtn = document.getElementById('getFileTree');
    const fileTreeDisplay = document.getElementById('fileTree');
    const promptInput = document.getElementById('prompt');
    const generatePlanBtn = document.getElementById('generatePlan');
    const planDisplay = document.getElementById('plan');
    const executePlanBtn = document.getElementById('executePlan');
    const resultDisplay = document.getElementById('result');

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

    function showError(message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error';
        errorDiv.textContent = message;
        document.body.appendChild(errorDiv);
        setTimeout(() => errorDiv.remove(), 5000);
    }
});
