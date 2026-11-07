import csv
import os

SAMPLE_DIR = "sample_data"


def check_columns(found_columns, needed_columns, file_path):
    if found_columns is None:
        raise ValueError(f"{file_path} is empty")
    missing = [name for name in needed_columns if name not in found_columns]
    if missing:
        raise ValueError(f"{file_path} is missing columns: {missing}")


def get_grade(average):
    if average >= 85:
        return "A"
    if average >= 70:
        return "B"
    if average >= 55:
        return "C"
    if average >= 40:
        return "D"
    return "F"


def id_sort_key(student_id):
    if student_id.isdigit():
        return (0, int(student_id), "")
    return (1, 0, student_id)


def read_students(path):
    students = {}
    with open(path, newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        check_columns(reader.fieldnames, ["student_id", "name"], path)
        for row in reader:
            student_id = (row.get("student_id") or "").strip()
            name = (row.get("name") or "").strip()
            if not student_id or not name:
                raise ValueError("students file has a row with empty id or name")
            if student_id in students:
                raise ValueError(f"Duplicate student id: {student_id}")
            students[student_id] = name
    return students


def read_scores(path, students):
    marks = {}
    rejected = []

    with open(path, newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        check_columns(reader.fieldnames, ["student_id", "subject", "marks"], path)

        for row_number, row in enumerate(reader, start=2):
            student_id = (row.get("student_id") or "").strip()
            subject = (row.get("subject") or "").strip()
            marks_text = (row.get("marks") or "").strip()
            reason = None

            if student_id not in students:
                reason = "Unknown student id"
            elif not subject:
                reason = "Subject is empty"
            else:
                try:
                    value = float(marks_text)
                except ValueError:
                    reason = "Marks is not a number"
                else:
                    if not 0 <= value <= 100:
                        reason = "Marks must be between 0 and 100"
                    elif subject.lower() in marks.get(student_id, {}):
                        reason = "Duplicate student-subject entry"

            if reason:
                rejected.append(f"Row {row_number} ({student_id}, {subject}, {marks_text}): {reason}")
            else:
                marks.setdefault(student_id, {})[subject.lower()] = value

    return marks, rejected


def build_report(students, marks):
    ranked = []
    for student_id, subject_marks in marks.items():
        average = round(sum(subject_marks.values()) / len(subject_marks), 2)
        ranked.append({
            "student_id": student_id,
            "name": students[student_id],
            "average": average,
            "grade": get_grade(average),
        })

    ranked.sort(key=lambda row: (-row["average"], id_sort_key(row["student_id"])))
    for position, row in enumerate(ranked, start=1):
        row["rank"] = position

    for student_id in sorted(students, key=id_sort_key):
        if student_id not in marks:
            ranked.append({"student_id": student_id, "name": students[student_id],
                           "average": "N/A", "grade": "N/A", "rank": "N/A"})
    return ranked


def write_report(path, report):
    with open(path, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file,
                                fieldnames=["student_id", "name", "average", "grade", "rank"])
        writer.writeheader()
        writer.writerows(report)


def create_sample_gradebook_files(students_path, scores_path):
    with open(students_path, "w", newline="", encoding="utf-8") as f:
        f.write("student_id,name\n101,Ali\n102,Sara\n103,Bilal\n104,Hina\n")
    with open(scores_path, "w", newline="", encoding="utf-8") as f:
        f.write("student_id,subject,marks\n"
                "101,Math,90\n101,Physics,80\n101,English,85\n"
                "102,Math,95\n102,Physics,88\n"
                "103,Math,45\n103,Physics,52\n"
                "101,Math,70\n"
                "999,Math,60\n"
                "102,English,120\n"
                "103,Urdu,abc\n")


def main():
    os.makedirs(SAMPLE_DIR, exist_ok=True)
    students_path = os.path.join(SAMPLE_DIR, "students.csv")
    scores_path = os.path.join(SAMPLE_DIR, "scores.csv")
    report_path = os.path.join(SAMPLE_DIR, "report.csv")

    create_sample_gradebook_files(students_path, scores_path)

    students = read_students(students_path)
    marks, rejected = read_scores(scores_path, students)
    report = build_report(students, marks)
    write_report(report_path, report)

    print(f"{'ID':<6}{'Name':<8}{'Average':<10}{'Grade':<7}Rank")
    for row in report:
        print(f"{row['student_id']:<6}{row['name']:<8}{str(row['average']):<10}"
              f"{row['grade']:<7}{row['rank']}")
    print("Rejected rows:")
    for msg in rejected:
        print("  ", msg)
    print("Report saved to report.csv")


if __name__ == "__main__":
    main()