import sqlite3

# Connect to database (file is created automatically)
conn = sqlite3.connect("students.db")
cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    m1 INTEGER, m2 INTEGER, m3 INTEGER
)
""")
conn.commit()


def get_grade(percentage):
    if percentage >= 90:
        return "A+"
    elif percentage >= 75:
        return "A"
    elif percentage >= 60:
        return "B"
    elif percentage >= 40:
        return "C"
    return "Fail"


def read_marks():
    marks = []
    for i in range(1, 4):
        m = int(input(f"Enter marks for subject {i} (0-100): "))
        if m < 0 or m > 100:
            raise ValueError("Marks must be between 0 and 100")
        marks.append(m)
    return marks


def show_row(row):
    sid, name, m1, m2, m3 = row
    total = m1 + m2 + m3
    percentage = total / 3
    print(f"ID:{sid} | {name} | Total:{total} | {percentage:.2f}% | Grade:{get_grade(percentage)}")


def add_student():
    name = input("Enter name: ").strip()
    m1, m2, m3 = read_marks()
    cur.execute("INSERT INTO students (name, m1, m2, m3) VALUES (?, ?, ?, ?)", (name, m1, m2, m3))
    conn.commit()
    print("Student added.")


def view_students():
    rows = cur.execute("SELECT * FROM students").fetchall()
    if not rows:
        print("No records found.")
    for row in rows:
        show_row(row)


def search_student():
    name = input("Enter name to search: ").strip()
    rows = cur.execute("SELECT * FROM students WHERE name LIKE ?", ("%" + name + "%",)).fetchall()
    if not rows:
        print("No student found.")
    for row in rows:
        show_row(row)


def update_student():
    sid = int(input("Enter student ID to update: "))
    m1, m2, m3 = read_marks()
    cur.execute("UPDATE students SET m1=?, m2=?, m3=? WHERE id=?", (m1, m2, m3, sid))
    conn.commit()
    print("Updated." if cur.rowcount else "ID not found.")


def delete_student():
    sid = int(input("Enter student ID to delete: "))
    cur.execute("DELETE FROM students WHERE id=?", (sid,))
    conn.commit()
    print("Deleted." if cur.rowcount else "ID not found.")


def show_topper():
    row = cur.execute("SELECT * FROM students ORDER BY (m1 + m2 + m3) DESC LIMIT 1").fetchone()
    if row:
        print("Topper:")
        show_row(row)
    else:
        print("No records found.")


def main():
    while True:
        print("\n--- Student Marks Manager ---")
        print("1. Add student")
        print("2. View all students")
        print("3. Search student")
        print("4. Update marks")
        print("5. Delete student")
        print("6. Show topper")
        print("7. Exit")
        choice = input("Choose an option: ")
        try:
            if choice == "1":
                add_student()
            elif choice == "2":
                view_students()
            elif choice == "3":
                search_student()
            elif choice == "4":
                update_student()
            elif choice == "5":
                delete_student()
            elif choice == "6":
                show_topper()
            elif choice == "7":
                print("Goodbye!")
                break
            else:
                print("Invalid choice.")
        except ValueError as e:
            print("Invalid input:", e)


main()
conn.close()
