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

    const uploadProgressBar = document.getElementById('uploadProgress');
    const progressBarFill = uploadProgressBar.querySelector('.progress');

    uploadFilesBtn.addEventListener('click', async () => {
        const formData = new FormData();
        const files = fileUploadInput.files;

        if (files.length === 0) {
            showError('Please select files or a directory to upload.');
            return;
        }

        for (const file of files) {
            const relativePath = file.webkitRelativePath || file.name;
            formData.append('files', file, relativePath);
        }

        try {
            uploadProgressBar.style.display = 'block';
            progressBarFill.style.width = '0%';

            const response = await fetch('/upload_files', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Failed to upload files');
            }

            const reader = response.body.getReader();
            const contentLength = +response.headers.get('Content-Length');

            let receivedLength = 0;
            let chunks = [];
            while(true) {
                const {done, value} = await reader.read();

                if (done) {
                    break;
                }

                chunks.push(value);
                receivedLength += value.length;
                const progress = Math.round((receivedLength / contentLength) * 100);
                progressBarFill.style.width = `${progress}%`;
            }

            const chunksAll = new Uint8Array(receivedLength);
            let position = 0;
            for(let chunk of chunks) {
                chunksAll.set(chunk, position);
                position += chunk.length;
            }

            const result = new TextDecoder("utf-8").decode(chunksAll);
            
            try {
                const data = JSON.parse(result);
                console.log('Parsed response:', data);
                console.log('File tree type:', typeof data.fileTree);
                console.log('File tree content:', data.fileTree);

                if (data.fileTree) {
                    if (typeof data.fileTree === 'object') {
                        fileTreeDisplay.textContent = JSON.stringify(data.fileTree, null, 2);
                    } else {
                        fileTreeDisplay.textContent = data.fileTree;
                    }
                    console.log('File tree display updated');
                } else {
                    console.error('File tree not found in the response');
                    fileTreeDisplay.textContent = 'Error: File tree not found in the response';
                }
            } catch (error) {
                console.error('Error parsing JSON:', error);
                showError('Error parsing server response');
            }
        } catch (error) {
            console.error('Error uploading files:', error);
            showError(error.message);
        } finally {
            uploadProgressBar.style.display = 'none';
        }
    });

    generatePlanBtn.addEventListener('click', async () => {
        const prompt = promptInput.value;
        if (!prompt) {
            showError('Please enter a prompt.');
            return;
        }

        try {
            generatePlanBtn.classList.add('loading');
            generatePlanBtn.disabled = true;

            const response = await fetch('/generate_plan', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ prompt })
            });

            if (!response.ok) throw new Error('Failed to generate plan');

            const data = await response.json();
            displayPlan(data);
        } catch (error) {
            showError(error.message);
        } finally {
            generatePlanBtn.classList.remove('loading');
            generatePlanBtn.disabled = false;
        }
    });

    executePlanBtn.addEventListener('click', async () => {
        const plan = JSON.parse(planDisplay.textContent);
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
            displayExecutionResult(data);
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

    function displayPlan(plan) {
        planDisplay.innerHTML = '';
        const planList = document.createElement('ol');
        plan.steps.forEach(step => {
            const listItem = document.createElement('li');
            listItem.textContent = step.description;
            const filesList = document.createElement('ul');
            step.files.forEach(file => {
                const fileItem = document.createElement('li');
                fileItem.textContent = file;
                filesList.appendChild(fileItem);
            });
            listItem.appendChild(filesList);
            planList.appendChild(listItem);
        });
        planDisplay.appendChild(planList);
        planDisplay.dataset.rawPlan = JSON.stringify(plan);
    }

    function displayExecutionResult(result) {
        resultDisplay.innerHTML = '';
        const resultList = document.createElement('ol');
        result.steps.forEach(step => {
            const listItem = document.createElement('li');
            listItem.textContent = step.description;
            const pre = document.createElement('pre');
            pre.textContent = step.content;
            listItem.appendChild(pre);
            resultList.appendChild(listItem);
        });
        resultDisplay.appendChild(resultList);
    }
});
