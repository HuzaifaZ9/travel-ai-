from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
import google.generativeai as genai

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)

# Configure Gemini API
genai.configure(api_key=os.getenv('GEMINI_API_KEY', 'AIzaSyB9fIgOxfM7RaQqtuGrkdyNe4D5MTjoluo'))

def construct_gemini_prompt(form_data):
    """Construct a detailed prompt for Gemini API"""
    return f"""
    Create a comprehensive travel itinerary with the following specifications:
    - Destination: {form_data['destination']}
    - Travel Dates: From {form_data['startDate']} to {form_data['endDate']}
    - Travel Type: {form_data['travelType']}
    - Budget Range: {form_data['budget']}
    - Additional Preferences: {form_data['additionalPreferences']}

    Please provide a detailed, day-by-day breakdown including:
    1. Daily activities and attractions
    2. Recommended restaurants and dining experiences
    3. Transportation suggestions
    4. Estimated costs for activities
    5. Travel tips specific to the destination and travel type

    Format the response in an easy-to-read HTML format with clear headings and lists.
    """

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate-itinerary', methods=['POST'])
def generate_itinerary():
    try:
        form_data = request.json

        # Validate input
        required_fields = ['destination', 'startDate', 'endDate', 'travelType', 'budget']
        for field in required_fields:
            if not form_data.get(field):
                return jsonify({
                    'error': f'Missing required field: {field}',
                    'status': 'error'
                }), 400

        # Generate model
        model = genai.GenerativeModel('gemini-pro')

        # Construct prompt
        prompt = construct_gemini_prompt(form_data)

        # Generate content
        response = model.generate_content(prompt)

        # Convert response to HTML for easy frontend rendering
        itinerary_html = response.text.replace('\n', '<br>')

        return jsonify({
            'itinerary': itinerary_html,
            'status': 'success'
        })

    except genai.types.generation_types.BlockedPromptException as e:
        return jsonify({
            'error': 'Prompt was blocked due to safety concerns.',
            'status': 'error'
        }), 400

    except Exception as e:
        print(f"Error generating itinerary: {e}")  # Log the full error
        return jsonify({
            'error': 'An unexpected error occurred while generating the itinerary.',
            'status': 'error'
        }), 500

if __name__ == '__main__':
    app.run(debug=True)