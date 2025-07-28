def generate_feedback(current_data, previous_terms=None, term="Current"):
    subjects = ['Nepali', 'English', 'Mathematics', 'Science', 'Social&Arts', 'Health_physical_CA', 'Computer']
    feedback = {
        'strengths': [], 'weaknesses': [], 'improvements': [],
        'recommendations': [], 'comparison': {}, 'behavioral_analysis': {},
        'summary': ''
    }

    for subject in subjects:
        score = current_data[subject]
        if score >= 80:
            feedback['strengths'].append(f"Excellent performance in {subject} ({score}%)")
        elif score >= 60:
            feedback['strengths'].append(f"Good performance in {subject} ({score}%)")
        elif score < 40:
            feedback['weaknesses'].append(f"Needs improvement in {subject} ({score}%)")
        else:
            feedback['weaknesses'].append(f"Average performance in {subject} ({score}%)")

    if current_data['Attendance'] < 75:
        feedback['weaknesses'].append(f"Poor attendance ({current_data['Attendance']}%)")
    elif current_data['Attendance'] >= 90:
        feedback['strengths'].append(f"Excellent attendance ({current_data['Attendance']}%)")

    if previous_terms:
        for term_name, prev_data in previous_terms.items():
            feedback['comparison'][term_name] = {}
            for subject in subjects:
                diff = current_data[subject] - prev_data[subject]
                if diff > 10:
                    feedback['comparison'][term_name][subject] = f"Significant improvement (+{diff})"
                    feedback['improvements'].append(f"Great improvement in {subject} from {term_name}")
                elif diff < -10:
                    feedback['comparison'][term_name][subject] = f"Significant decline ({diff})"
                    feedback['weaknesses'].append(f"Declined in {subject} from {term_name}")
                else:
                    feedback['comparison'][term_name][subject] = f"Stable ({diff:+})"

    weak_subjects = [s for s in subjects if current_data[s] < 50]
    if weak_subjects:
        feedback['recommendations'].append(f"Focus on: {', '.join(weak_subjects)}")
        feedback['recommendations'].append("Seek help or tutoring in weak subjects")

    if current_data['Attendance'] < 85:
        feedback['recommendations'].append("Improve class attendance")

    strong_subjects = [s for s in subjects if current_data[s] >= 80]
    if strong_subjects:
        feedback['recommendations'].append(f"Maintain excellence in: {', '.join(strong_subjects)}")

    # Behavioral Analysis
    behavioral_issues = []
    behavioral_strengths = []

    # Analyze Late Coming
    if 'Late_Coming_Frequency' in current_data:
        if current_data['Late_Coming_Frequency'] == 'Often':
            behavioral_issues.append("frequently comes to class late")
            feedback['weaknesses'].append("Poor punctuality - often comes to class late")
            feedback['recommendations'].append("Improve punctuality and arrive to class on time")
        elif current_data['Late_Coming_Frequency'] == 'Sometimes':
            feedback['recommendations'].append("Work on being more consistent with punctuality")
        else:  # Rarely
            behavioral_strengths.append("good punctuality")
            feedback['strengths'].append("Excellent punctuality - rarely late to class")

    # Analyze Assignment Submission
    if 'Assignment_Submission' in current_data:
        if current_data['Assignment_Submission'] == 'Irregular':
            behavioral_issues.append("irregular assignment submission")
            feedback['weaknesses'].append("Inconsistent with assignment submissions")
            feedback['recommendations'].append("Develop better time management for assignment completion")
        else:  # Regular
            behavioral_strengths.append("regular assignment submission")
            feedback['strengths'].append("Consistent with assignment submissions")

    # Analyze Class Attention
    if 'Class_Attention' in current_data:
        if current_data['Class_Attention'] == 'Distracted':
            behavioral_issues.append("does not pay attention in class")
            feedback['weaknesses'].append("Lacks focus and attention during class")
            feedback['recommendations'].append("Improve concentration and active participation in class")
        else:  # Attentive
            behavioral_strengths.append("pays good attention in class")
            feedback['strengths'].append("Shows good attention and focus during class")

    # Analyze Responsibility
    if 'Responsibility_Behavior' in current_data:
        if current_data['Responsibility_Behavior'] == 'Irresponsible':
            behavioral_issues.append("shows irresponsible behavior")
            feedback['weaknesses'].append("Demonstrates irresponsible behavior in school")
            feedback['recommendations'].append("Develop more responsible attitudes and behavior")
        else:  # Responsible
            behavioral_strengths.append("responsible behavior")
            feedback['strengths'].append("Shows responsible behavior and attitude")

    # Store behavioral analysis
    feedback['behavioral_analysis'] = {
        'issues': behavioral_issues,
        'strengths': behavioral_strengths
    }

    # Generate comprehensive summary
    total_marks = sum([current_data[s] for s in subjects])
    percentage = (total_marks / 700) * 100

    # Performance level
    if percentage >= 80:
        performance_level = "excellent"
    elif percentage >= 70:
        performance_level = "good"
    elif percentage >= 60:
        performance_level = "satisfactory"
    elif percentage >= 40:
        performance_level = "below average"
    else:
        performance_level = "poor"

    # Create summary
    summary_parts = []

    if percentage < 60:  # Below satisfactory performance
        summary_parts.append(f"The student has not performed well in this {term.lower()}, achieving {performance_level} results with {percentage:.1f}%.")

        if behavioral_issues:
            if len(behavioral_issues) == 1:
                summary_parts.append(f"This poor performance can be attributed to the fact that the student {behavioral_issues[0]}.")
            else:
                issues_text = ", ".join(behavioral_issues[:-1]) + f", and {behavioral_issues[-1]}"
                summary_parts.append(f"This poor performance can be attributed to multiple behavioral issues: the student {issues_text}.")

        summary_parts.append("The student should focus on improving these behavioral aspects along with academic studies to achieve better results.")

    else:  # Good performance
        summary_parts.append(f"The student has achieved {performance_level} results in this {term.lower()} with {percentage:.1f}%.")

        if behavioral_strengths:
            strengths_text = ", ".join(behavioral_strengths)
            summary_parts.append(f"This good performance is supported by positive behaviors including {strengths_text}.")

        if behavioral_issues:
            issues_text = ", ".join(behavioral_issues)
            summary_parts.append(f"However, there are some areas for improvement: the student {issues_text}.")
            summary_parts.append("Addressing these behavioral concerns could lead to even better academic performance.")

    feedback['summary'] = " ".join(summary_parts)

    return feedback
