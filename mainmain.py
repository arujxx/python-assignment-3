import os
import csv
import json


class FileManager:
    def __init__(self, filename):
        self.filename = filename

    def check_file(self):
        print("Checking file...")

        if os.path.exists(self.filename):
            print("File found:", self.filename)
            return True
        else:
            print("Error:", self.filename, "not found. Please check the filename.")
            return False

    def create_output_folder(self, folder="output"):
        print("Checking output folder...")

        if os.path.exists(folder):
            print("Output folder already exists:", folder + "/")
        else:
            os.makedirs(folder)
            print("Output folder created:", folder + "/")


class DataLoader:
    def __init__(self, filename):
        self.filename = filename
        self.students = []

    def load(self):
        print("Loading data...")

        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)

                for row in reader:
                    self.students.append(row)

            print("Data loaded successfully:", len(self.students), "students")
            return self.students

        except FileNotFoundError:
            print("Error: File '" + self.filename + "' not found. Please check the filename.")
            return []

        except Exception as error:
            print("Error while loading data:", error)
            return []

    def preview(self, n=5):
        print("First", n, "rows:")
        print("-" * 30)

        for i in range(n):
            student = self.students[i]
            print(
                student["student_id"],
                "|",
                student["age"],
                "|",
                student["gender"],
                "|",
                student["country"],
                "| GPA:",
                student["GPA"]
            )

        print("-" * 30)


class DataAnalyser:
    def __init__(self, students):
        self.students = students
        self.result = {}

    def analyse(self):
        low_sleep_gpas = []
        high_sleep_gpas = []

        for student in self.students:
            try:
                sleep_hours = float(student["sleep_hours"])
                gpa = float(student["GPA"])

                if sleep_hours < 6:
                    low_sleep_gpas.append(gpa)
                else:
                    high_sleep_gpas.append(gpa)

            except ValueError:
                print("Warning: could not convert value for student", student["student_id"], "— skipping row.")
                continue

        low_avg = round(sum(low_sleep_gpas) / len(low_sleep_gpas), 2)
        high_avg = round(sum(high_sleep_gpas) / len(high_sleep_gpas), 2)
        difference = round(high_avg - low_avg, 2)

        self.result = {
            "analysis": "Sleep vs GPA",
            "total_students": len(self.students),
            "low_sleep": {
                "students": len(low_sleep_gpas),
                "avg_gpa": low_avg
            },
            "high_sleep": {
                "students": len(high_sleep_gpas),
                "avg_gpa": high_avg
            },
            "gpa_difference": difference
        }

        return self.result

    def print_results(self):
        print("-" * 30)
        print("Sleep vs GPA Analysis")
        print("-" * 30)
        print("Students sleeping < 6 hours :", self.result["low_sleep"]["students"])
        print("Average GPA (< 6 hours) :", self.result["low_sleep"]["avg_gpa"])
        print("Students sleeping >= 6 hours :", self.result["high_sleep"]["students"])
        print("Average GPA (>= 6 hours) :", self.result["high_sleep"]["avg_gpa"])
        print("Difference in avg GPA :", self.result["gpa_difference"])
        print("-" * 30)

    def lambda_filter_analysis(self):
        print("-" * 30)
        print("Lambda / Map / Filter")
        print("-" * 30)

        low_sleep = list(filter(lambda s: float(s["sleep_hours"]) < 6, self.students))
        gpa_values = list(map(lambda s: float(s["GPA"]), self.students))
        stressed = list(filter(lambda s: float(s["mental_stress_level"]) > 7, self.students))

        print("Students with sleep < 6 hrs :", len(low_sleep))
        print("GPA values (first 5) :", gpa_values[:5])
        print("Students with stress > 7 :", len(stressed))
        print("-" * 30)


class ResultSaver:
    def __init__(self, result, output_path):
        self.result = result
        self.output_path = output_path

    def save_json(self):
        try:
            with open(self.output_path, "w", encoding="utf-8") as file:
                json.dump(self.result, file, indent=4)

            print("Result saved to", self.output_path)

        except Exception as error:
            print("Error while saving result:", error)


def main():
    filename = "students.csv"

    fm = FileManager(filename)

    if not fm.check_file():
        print("Stopping program.")
        return

    fm.create_output_folder()

    dl = DataLoader(filename)
    dl.load()
    dl.preview()

    analyser = DataAnalyser(dl.students)
    analyser.analyse()
    analyser.print_results()
    analyser.lambda_filter_analysis()

    saver = ResultSaver(analyser.result, "output/result.json")
    saver.save_json()


main()
