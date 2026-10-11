"""
The class data for Lab 3. These are FICTIONAL students.

Each student is a dictionary:
    name      the student's first name
    year      1, 2, 3 or 4
    langs     a set of programming languages the student knows, e.g. {"Python", "C"}
    github    True if the student has a GitHub account
    math      the student's grade in Math I, from 0 to 100

Do not change this file: the tests also use other, hidden data sets of the same shape.
"""

STUDENTS = [
    {"name": "Ada",    "year": 2, "langs": {"Python", "C"},          "github": True,  "math": 92},
    {"name": "Bora",   "year": 1, "langs": {"Python"},               "github": True,  "math": 67},
    {"name": "Cemre",  "year": 2, "langs": {"Python", "Java"},       "github": True,  "math": 74},
    {"name": "Doruk",  "year": 3, "langs": {"Java", "C", "SQL"},     "github": False, "math": 58},
    {"name": "Ece",    "year": 1, "langs": {"C"},                    "github": True,  "math": 81},
    {"name": "Fırat",  "year": 2, "langs": {"Java"},                 "github": True,  "math": 49},
    {"name": "Gizem",  "year": 4, "langs": {"Python", "SQL"},        "github": True,  "math": 88},
    {"name": "Hakan",  "year": 1, "langs": set(),                    "github": False, "math": 55},
    {"name": "Irmak",  "year": 3, "langs": {"Python", "Java", "C"},  "github": True,  "math": 95},
    {"name": "Kaan",   "year": 2, "langs": {"Python"},               "github": False, "math": 62},
]
