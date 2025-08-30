def calculate_grade(marks):
    if marks >= 90:
        return "A+"
    elif marks >= 80:
        return "A"
    elif marks >= 70:
        return "B"
    elif marks >= 60:
        return "C"
    elif marks >= 50:
        return "D"
    else:
        return "F"

def student_grading():
    subjects = int(input("Enter number of subjects: "))

    subject_names = []
    for i in range(subjects):
        name = input(f"Enter name of subject {i+1}: ")
        subject_names.append(name)

    student_record = {}
    for subject in subject_names:
        marks = int(input(f"Enter marks obtained in {subject} (out of 100): "))
        grade = calculate_grade(marks)
        student_record[subject] = {"Marks": marks, "Grade": grade}

    print("\nStudent Report Card:")
    for subject, details in student_record.items():
        print(f"{subject} marks = {details['Marks']} , grade = {details['Grade']}")

    avg_marks = sum([details["Marks"] for details in student_record.values()]) / subjects
    print(f"\nOverall Average = {avg_marks:.2f}")
    print(f"Final Grade = {calculate_grade(avg_marks)}")

student_grading()

