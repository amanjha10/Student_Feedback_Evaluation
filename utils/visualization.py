
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import numpy as np
import io
import base64

def create_visualizations(current_data, previous_terms=None, student_name="Student"):
    subjects = ['Nepali', 'English', 'Mathematics', 'Science', 'Social&Arts', 'Health_physical_CA', 'Computer']

    # Determine the number of subplots needed
    if previous_terms and len(previous_terms) > 0:
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle(f"{student_name}'s Performance Analysis", fontsize=18, fontweight='bold')

        # Current term performance (top-left)
        ax1 = axes[0, 0]
        marks = [current_data[s] for s in subjects]
        colors = ['green' if m >= 80 else 'orange' if m >= 60 else 'red' if m < 40 else 'blue' for m in marks]
        bars = ax1.bar(subjects, marks, color=colors)
        ax1.axhline(y=40, color='red', linestyle='--', label='Pass Line', alpha=0.7)
        ax1.set_title('Current Term Performance', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Marks')
        ax1.set_xticks(range(len(subjects)))
        ax1.set_xticklabels(subjects, rotation=45, ha='right')
        ax1.legend()
        ax1.set_ylim(0, 100)
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 1, f'{int(height)}', ha='center', fontweight='bold')

        # Comparison chart (top-right)
        ax2 = axes[0, 1]
        current_marks = [current_data[s] for s in subjects]

        # Get the most recent previous term for comparison
        latest_term = list(previous_terms.keys())[-1]
        previous_marks = [previous_terms[latest_term][s] for s in subjects]

        x = np.arange(len(subjects))
        width = 0.35

        bars1 = ax2.bar(x - width/2, current_marks, width, label='Current Term', color='skyblue', alpha=0.8)
        bars2 = ax2.bar(x + width/2, previous_marks, width, label=f'{latest_term}', color='lightcoral', alpha=0.8)

        ax2.set_title(f'Comparison: Current vs {latest_term}', fontsize=14, fontweight='bold')
        ax2.set_ylabel('Marks')
        ax2.set_xticks(x)
        ax2.set_xticklabels(subjects, rotation=45, ha='right')
        ax2.legend()
        ax2.axhline(y=40, color='red', linestyle='--', alpha=0.7)
        ax2.set_ylim(0, 100)

        # Add value labels on bars
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                ax2.text(bar.get_x() + bar.get_width()/2., height + 1, f'{int(height)}',
                        ha='center', va='bottom', fontsize=9)

        # Progress trend chart (bottom-left)
        ax3 = axes[1, 0]
        all_terms = list(previous_terms.keys()) + ['Current']

        for subject in subjects[:4]:  # Show top 4 subjects to avoid clutter
            term_marks = []
            for term in previous_terms.keys():
                term_marks.append(previous_terms[term][subject])
            term_marks.append(current_data[subject])

            ax3.plot(all_terms, term_marks, marker='o', linewidth=2, label=subject)

        ax3.set_title('Progress Trend (Top 4 Subjects)', fontsize=14, fontweight='bold')
        ax3.set_ylabel('Marks')
        ax3.set_xlabel('Terms')
        ax3.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        ax3.grid(True, alpha=0.3)
        ax3.axhline(y=40, color='red', linestyle='--', alpha=0.7)
        plt.setp(ax3.get_xticklabels(), rotation=45, ha='right')

        # Overall performance comparison (bottom-right)
        ax4 = axes[1, 1]
        term_totals = []
        term_percentages = []

        for term in previous_terms.keys():
            total = sum([previous_terms[term][s] for s in subjects])
            percentage = (total / 700) * 100
            term_totals.append(total)
            term_percentages.append(percentage)

        current_total = sum([current_data[s] for s in subjects])
        current_percentage = (current_total / 700) * 100
        term_totals.append(current_total)
        term_percentages.append(current_percentage)

        colors = ['lightblue' if i < len(all_terms)-1 else 'darkblue' for i in range(len(all_terms))]
        bars = ax4.bar(all_terms, term_percentages, color=colors, alpha=0.8)
        ax4.set_title('Overall Performance Trend', fontsize=14, fontweight='bold')
        ax4.set_ylabel('Percentage (%)')
        ax4.set_xlabel('Terms')
        ax4.axhline(y=40, color='red', linestyle='--', label='Pass Line', alpha=0.7)
        ax4.axhline(y=80, color='green', linestyle='--', label='Excellence Line', alpha=0.7)
        ax4.legend()
        plt.setp(ax4.get_xticklabels(), rotation=45, ha='right')

        for bar in bars:
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width()/2., height + 1, f'{height:.1f}%',
                    ha='center', va='bottom', fontweight='bold')

    else:
        # Single chart for current term only
        fig, axes = plt.subplots(1, 1, figsize=(12, 8))
        fig.suptitle(f"{student_name}'s Subject-wise Marks", fontsize=16, fontweight='bold')

        marks = [current_data[s] for s in subjects]
        colors = ['green' if m >= 80 else 'orange' if m >= 60 else 'red' if m < 40 else 'blue' for m in marks]
        bars = axes.bar(subjects, marks, color=colors, alpha=0.8)
        axes.axhline(y=40, color='red', linestyle='--', label='Pass Line', alpha=0.7)
        axes.set_ylabel('Marks')
        axes.set_xticks(range(len(subjects)))
        axes.set_xticklabels(subjects, rotation=45, ha='right')
        axes.legend()
        axes.set_ylim(0, 100)
        for bar in bars:
            height = bar.get_height()
            axes.text(bar.get_x() + bar.get_width()/2., height + 1, f'{int(height)}',
                     ha='center', fontweight='bold')

    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=150, bbox_inches='tight')
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode("utf-8")
    plt.close()
    return img_str
