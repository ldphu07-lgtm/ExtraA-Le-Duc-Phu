import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "gradebook.json")


class GradebookManager:
    def __init__(self):
        self.courses = self.load_data()

    def load_data(self):
        if not os.path.exists(DATA_FILE):
            return []
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []

    def save_data(self):
        try:
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.courses, f, indent=4)
            print(">> Data saved successfully!")
        except IOError:
            print(">> Error: Could not save data.")

    def add_course(self, code, name, credits, semester, score):
        for course in self.courses:
            if course['code'] == code:
                return False, "The course code already exists!"

        new_course = {
            "code": code,
            "name": name,
            "credits": credits,
            "semester": semester,
            "score": score
        }
        self.courses.append(new_course)
        self.save_data()
        return True, "Course added successfully."

    def update_course(self, code, new_data):
        for course in self.courses:
            if course['code'] == code:
                course.update(new_data)
                self.save_data()
                return True
        return False

    def delete_course(self, code):
        initial_count = len(self.courses)
        self.courses = [c for c in self.courses if c['code'] != code]
        if len(self.courses) < initial_count:
            self.save_data()
            return True
        return False

    def get_all_courses(self):
        return self.courses

    def calculate_gpa(self, semester=None):
        total_points = 0
        total_credits = 0
        target_courses = self.courses

        if semester:
            target_courses = [
                c for c in self.courses if c['semester'] == semester]

        for c in target_courses:
            total_points += c['score'] * c['credits']
            total_credits += c['credits']

        if total_credits == 0:
            return 0.0

        return round(total_points / total_credits, 2)
