document.getElementById('pharmacistForm').addEventListener('submit', async (event) => {
    event.preventDefault();

    const action = document.getElementById('action').value;
    const input = document.getElementById('input').value.trim();
    const fileUpload = document.getElementById('fileUpload').files[0];
    const responseDiv = document.getElementById('response');
    responseDiv.innerHTML = 'Loading...';

    let fetchOptions = {
        method: 'POST',
    };

    // Check if the user has uploaded a file or provided text input
    if (fileUpload) {
        // Prepare FormData for file upload
        let formData = new FormData();
        formData.append('file', fileUpload);
        formData.append('action', action); // Append action to FormData for server-side logic
        fetchOptions.body = formData;
    } else if (input) {
        // Prepare JSON payload for text input
        let payload = {
            action: action, // Include the action in the JSON payload
            input: input,   // Rename 'input' to match server expectation
        };
        fetchOptions.headers = { 'Content-Type': 'application/json' };
        fetchOptions.body = JSON.stringify(payload);
    } else {
        alert('Please provide input or upload a file.');
        responseDiv.innerHTML = '';
        return;
    }

    try {
        const response = await fetch('/upload_and_process_image', fetchOptions);
        const data = await response.json();
        responseDiv.innerHTML = data.success ? data.response.replace(/\n/g, '<br>') : `An error occurred: ${data.error}. Please try again.`;
    } catch (error) {
        responseDiv.innerHTML = `An error occurred: ${error.message}. Please try again.`;
        console.error(error);
    }
});
