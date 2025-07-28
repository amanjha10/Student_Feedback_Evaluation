
from flask import Flask, render_template, request
from utils.data_loader import load_student_data
from utils.metrics import calculate_metrics
from utils.feedback import generate_feedback
from utils.visualization import create_visualizations
from utils.model import train_prediction_model, predict_with_behavioral_factors

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_student():
    try:
        # Get form data
        student_data = {
            'Name': request.form['name'],
            'Email': request.form['email'],
            'Nepali': int(request.form['nepali']),
            'English': int(request.form['english']),
            'Mathematics': int(request.form['mathematics']),
            'Science': int(request.form['science']),
            'Social&Arts': int(request.form['social_arts']),
            'Health_physical_CA': int(request.form['health_physical']),
            'Computer': int(request.form['computer']),
            'Attendance': int(request.form['attendance']),
            'Late_Coming_Frequency': request.form['late_coming'],
            'Assignment_Submission': request.form['assignment_submission'],
            'Class_Attention': request.form['class_attention'],
            'Responsibility_Behavior': request.form['responsibility']
        }

        term = request.form.get('term', 'Current')
        previous_terms = {}
        if request.form.get('has_previous_terms') == 'yes':
            previous_term_names = request.form.getlist('previous_term_name[]')
            for i, term_name in enumerate(previous_term_names):
                if term_name:
                    try:
                        previous_terms[term_name] = {
                            'Nepali': int(request.form.getlist('prev_nepali[]')[i]),
                            'English': int(request.form.getlist('prev_english[]')[i]),
                            'Mathematics': int(request.form.getlist('prev_mathematics[]')[i]),
                            'Science': int(request.form.getlist('prev_science[]')[i]),
                            'Social&Arts': int(request.form.getlist('prev_social_arts[]')[i]),
                            'Health_physical_CA': int(request.form.getlist('prev_health_physical[]')[i]),
                            'Computer': int(request.form.getlist('prev_computer[]')[i]),
                            'Attendance': int(request.form.getlist('prev_attendance[]')[i]),
                            'Late_Coming_Frequency': request.form.getlist('prev_late_coming[]')[i],
                            'Assignment_Submission': request.form.getlist('prev_assignment_submission[]')[i],
                            'Class_Attention': request.form.getlist('prev_class_attention[]')[i],
                            'Responsibility_Behavior': request.form.getlist('prev_responsibility[]')[i]
                        }
                    except (IndexError, ValueError):
                        continue

        total, percentage, status = calculate_metrics(student_data)
        feedback = generate_feedback(student_data, previous_terms, term)
        chart_img = create_visualizations(student_data, previous_terms, student_data['Name'])

        model, model_accuracy, label_encoders = train_prediction_model()
        predicted_total = predict_with_behavioral_factors(model, label_encoders, student_data)

        if percentage >= 90:
            grade = "A+"
        elif percentage >= 80:
            grade = "A"
        elif percentage >= 70:
            grade = "B+"
        elif percentage >= 60:
            grade = "B"
        elif percentage >= 50:
            grade = "C+"
        elif percentage >= 40:
            grade = "C"
        else:
            grade = "F"

        result = {
            'student_data': student_data,
            'total': total,
            'percentage': round(percentage, 2),
            'status': status,
            'grade': grade,
            'feedback': feedback,
            'chart': chart_img,
            'predicted_total': round(predicted_total, 1),
            'model_accuracy': round(model_accuracy, 2),
            'term': term,
            'has_previous_terms': bool(previous_terms)
        }

        return render_template('result.html', result=result)

    except Exception as e:
        return f"Error processing data: {str(e)}", 400

if __name__ == '__main__':
    app.run(debug=True)
