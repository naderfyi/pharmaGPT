document.getElementById('pharmacistForm').addEventListener('submit', async (event) => {
    event.preventDefault();

    const action = document.getElementById('action').value;
    const input = document.getElementById('input').value.trim();
    if (!input) {
        alert('Input is required.');
        return;
    }

    const responseDiv = document.getElementById('response');
    responseDiv.innerHTML = 'Loading...';

    let payload = {};
    switch (action) {
        case 'analyze_prescription':
        case 'validate_prescription':
            payload = { prescription_text: input };
            break;
        case 'get_drug_information':
        case 'search_drug_or_condition':
            payload = { drug_name: input };
            break;
        case 'check_drug_interactions':
            payload = { drug_list: input.split(',').map(drug => drug.trim()) };
            break;
    }

    try {
        const response = await fetch(`/${action}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const data = await response.json();
        responseDiv.innerHTML = data.success ? data.response.replace(/\n/g, '<br>') : `An error occurred: ${error.message}. Please try again.`;
    } catch (error) {
        responseDiv.innerHTML = `An error occurred: ${error.message}. Please try again.`;
        console.error(error);
    }
});