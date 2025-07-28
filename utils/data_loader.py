
import pandas as pd

def load_student_data():
    """Load student data from Excel file with behavioral characteristics"""
    df = pd.read_excel('data/student_feedback_evaluation.xlsx')
    return df

def get_behavioral_fields():
    """Return the list of behavioral fields available in the dataset"""
    return ['Late_Coming_Frequency', 'Assignment_Submission', 'Class_Attention', 'Responsibility_Behavior']

def get_academic_subjects():
    """Return the list of academic subjects"""
    return ['Nepali', 'English', 'Mathematics', 'Science', 'Social&Arts', 'Health_physical_CA', 'Computer']
