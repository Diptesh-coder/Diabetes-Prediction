document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('prediction-form');
    const resultContainer = document.getElementById('result');
    const predictionText = document.querySelector('.prediction-text');
    const probabilityText = document.querySelector('.probability-text');
    const meterFill = document.querySelector('.meter-fill');
    const resultExplanation = document.querySelector('.result-explanation');

    form.addEventListener('submit', async function(e) {
        e.preventDefault();

        // Get form data
        const formData = new FormData(form);
        
        try {
            // Send prediction request
            const response = await fetch('/predict', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();

            if (result.error) {
                throw new Error(result.error);
            }

            // Update UI with prediction results
            updateResult(result);

        } catch (error) {
            alert('Error: ' + error.message);
        }
    });

    function updateResult(result) {
        const probability = result.probability;
        const prediction = result.prediction;

        // Show result container
        resultContainer.classList.remove('hidden');

        // Update prediction text
        predictionText.textContent = prediction === 1 
            ? 'Higher Risk of Diabetes'
            : 'Lower Risk of Diabetes';

        // Update probability text
        probabilityText.textContent = `Probability: ${probability}%`;

        // Update risk meter
        meterFill.style.width = `${probability}%`;

        // Update colors based on risk level
        resultContainer.className = 'result-container';
        if (probability < 30) {
            resultContainer.classList.add('low-risk');
            resultExplanation.textContent = 'Your risk level is low. However, maintaining a healthy lifestyle is always important.';
        } else if (probability < 70) {
            resultContainer.classList.add('medium-risk');
            resultExplanation.textContent = 'Your risk level is moderate. Consider consulting a healthcare provider for a thorough evaluation.';
        } else {
            resultContainer.classList.add('high-risk');
            resultExplanation.textContent = 'Your risk level is high. Please consult a healthcare provider for proper evaluation and guidance.';
        }

        // Scroll to result
        resultContainer.scrollIntoView({ behavior: 'smooth' });
    }

    // Input validation
    const inputs = form.querySelectorAll('input[type="number"]');
    inputs.forEach(input => {
        input.addEventListener('input', function() {
            const value = parseFloat(this.value);
            const min = parseFloat(this.min);
            const max = parseFloat(this.max);

            if (value < min) this.value = min;
            if (value > max) this.value = max;
        });
    });
});
