import pandas as pd

health_db = pd.read_csv("health_dataset.csv")

health_db = health_db.drop(columns=["student_id", "gender", "age", "parental_education_level", 
                            "attendance_percentage", "internet_quality", "exam_score"])

health_db.to_csv("reduced_health_dataset.csv", index = False)