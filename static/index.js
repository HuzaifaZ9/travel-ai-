document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('tripPlannerForm');
    const itineraryResult = document.getElementById('itineraryResult');
    const itineraryContent = document.getElementById('itineraryContent');
    const loadingSpinner = document.getElementById('loadingSpinner');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Show loading spinner
        loadingSpinner.classList.remove('hidden');
        itineraryResult.classList.add('hidden');

        // Collect form data
        const formData = {
            destination: document.getElementById('destination').value,
            startDate: document.getElementById('startDate').value,
            endDate: document.getElementById('endDate').value,
            travelType: document.getElementById('travelType').value,
            budget: document.getElementById('budget').value,
            additionalPreferences: document.getElementById('additionalPreferences').value
        };

        try {
            // Send data to backend
            const response = await fetch('/generate-itinerary', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });

            if (!response.ok) {
                throw new Error('Failed to generate itinerary');
            }

            const data = await response.json();

            // Hide loading spinner
            loadingSpinner.classList.add('hidden');

            // Display itinerary
            itineraryContent.innerHTML = data.itinerary;
            itineraryResult.classList.remove('hidden');

        } catch (error) {
            console.error('Error:', error);
            loadingSpinner.classList.add('hidden');
            itineraryContent.innerHTML = '<p>Error generating itinerary. Please try again.</p>';
            itineraryResult.classList.remove('hidden');
        }
    });
});