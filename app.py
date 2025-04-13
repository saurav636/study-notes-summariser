from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os

app = Flask(__name__)

# Configure Gemini API
GEMINI_API_KEY = "AIzaSyDEi95btI2y9fQOLn_HO9Atf92xkqvBhAo"
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/')
def home():
    try:
        return render_template('index.html')
    except Exception as e:
        return f"Error loading template: {str(e)}", 500

@app.route('/summarize', methods=['POST'])
def summarize():
    try:
        # Get the notes from the request
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        notes = data.get('notes', '')
        if not notes:
            return jsonify({'error': 'No notes provided'}), 400

        # Generate summary
        summary_prompt = f"""Please provide a concise summary of these study notes, extract key concepts, and generate 3 quiz questions with answers. Here are the notes:

{notes}

Please format your response as follows:
SUMMARY:
[Your summary here]

KEY CONCEPTS:
- [Concept 1]
- [Concept 2]
- [etc.]

QUIZ QUESTIONS:
1. [Question 1]
   Answer: [Answer 1]

2. [Question 2]
   Answer: [Answer 2]

3. [Question 3]
   Answer: [Answer 3]"""

        # Generate content with error handling
        try:
            response = model.generate_content(summary_prompt)
            if not response.text:
                return jsonify({'error': 'No response from AI model'}), 500
            return jsonify({'response': response.text})
        except Exception as ai_error:
            print(f"AI Model Error: {str(ai_error)}")
            return jsonify({'error': f'AI model error: {str(ai_error)}'}), 500
    
    except Exception as e:
        print(f"Server Error: {str(e)}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500

if __name__ == '__main__':
    # Get port from environment variable or use default
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port) 