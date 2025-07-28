
def calculate_metrics(row):
    subjects = ['Nepali', 'English', 'Mathematics', 'Science', 'Social&Arts', 'Health_physical_CA', 'Computer']
    total = sum([row[subject] for subject in subjects])
    percentage = (total / 700) * 100

    subject_pass = all([row[subject] >= 40 for subject in subjects])
    overall_pass = percentage >= 40
    attendance_pass = row['Attendance'] >= 75

    status = "PASS" if (subject_pass and overall_pass and attendance_pass) else "FAIL"
    return total, percentage, status
