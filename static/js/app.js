document.addEventListener('DOMContentLoaded', () => {
    const fileUploadInput = document.getElementById('fileUpload');
    const uploadFilesBtn = document.getElementById('uploadFiles');
    const fileTreeDisplay = document.getElementById('fileTree');
    const promptInput = document.getElementById('prompt');
    const generatePlanBtn = document.getElementById('generatePlan');
    const planDisplay = document.getElementById('plan');
    const executePlanBtn = document.getElementById('executePlan');
    const resultDisplay = document.getElementById('result');

    const gitInitBtn = document.getElementById('gitInit');
    const gitAddBtn = document.getElementById('gitAdd');
    const gitCommitBtn = document.getElementById('gitCommit');
    const commitMessageInput = document.getElementById('commitMessage');
    const gitStatusBtn = document.getElementById('gitStatus');
    const gitResultDisplay = document.getElementById('gitResult');

    uploadFilesBtn.addEventListener('click', async () => {
        const formData = new FormData();
        for (const file of fileUploadInput.files) {
            formData.append('files', file);
        }

        try {
            const response = await fetch('/upload_files', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) throw new Error('Failed to upload files');

            const data = await response.json();
            fileTreeDisplay.textContent = JSON.stringify(data.fileTree, null, 2);
        } catch (error) {
            showError(error.message);
        }
    });

    generatePlanBtn.addEventListener('click', async () => {
        const prompt = promptInput.value;
        if (!prompt) {
            showError('Please enter a prompt.');
            return;
        }

        try {
            const response = await fetch('/generate_plan', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ prompt })
            });

            if (!response.ok) throw new Error('Failed to generate plan');

            const data = await response.json();
            planDisplay.textContent = data.plan;
        } catch (error) {
            showError(error.message);
        }
    });

    executePlanBtn.addEventListener('click', async () => {
        const plan = planDisplay.textContent;
        if (!plan) {
            showError('Please generate a plan first.');
            return;
        }

        try {
            const response = await fetch('/execute_plan', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ plan })
            });

            if (!response.ok) throw new Error('Failed to execute plan');

            const data = await response.json();
            resultDisplay.textContent = JSON.stringify(data.result, null, 2);
        } catch (error) {
            showError(error.message);
        }
    });

    gitInitBtn.addEventListener('click', async () => {
        try {
            const response = await fetch('/git_init', { method: 'POST' });
            if (!response.ok) throw new Error('Failed to initialize Git repository');
            const data = await response.json();
            gitResultDisplay.textContent = data.result;
        } catch (error) {
            showError(error.message);
        }
    });

    gitAddBtn.addEventListener('click', async () => {
        try {
            const response = await fetch('/git_add', { method: 'POST' });
            if (!response.ok) throw new Error('Failed to stage changes');
            const data = await response.json();
            gitResultDisplay.textContent = data.result;
        } catch (error) {
            showError(error.message);
        }
    });

    gitCommitBtn.addEventListener('click', async () => {
        const message = commitMessageInput.value;
        if (!message) {
            showError('Please enter a commit message.');
            return;
        }

        try {
            const response = await fetch('/git_commit', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message })
            });
            if (!response.ok) throw new Error('Failed to commit changes');
            const data = await response.json();
            gitResultDisplay.textContent = data.result;
        } catch (error) {
            showError(error.message);
        }
    });

    gitStatusBtn.addEventListener('click', async () => {
        try {
            const response = await fetch('/git_status', { method: 'POST' });
            if (!response.ok) throw new Error('Failed to get Git status');
            const data = await response.json();
            gitResultDisplay.textContent = data.result;
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
