#
l_numbers = [list(range(1, 101))]

#
r_numbers = range(1, 101)

#
t_key_numbers = (
    (1, "one"),
    (2, "Two"),
    (3, "Three"),
    (4, "Four"),
    (5, "Five"),
    (6, "Six"),
    (7, "Seven"),
    (8, "Eight"),
    (9, "Nine"),
    (10, "Ten"),
    (11, "Eleven"),
    (12, "Twelve"),
    (13, "Thirteen"),
    (14, "Fourteen"),
    (15, "Fifteen"),
    (16, "Sixteen")
)

#
t_key_values = (
    ("ABC", 10.5),
    ("XYZ", 23.8),
    ("ABC", 11.2),
    ("XYZ", 20.3),
    ("ABC", 10.7),
    ("XYZ", 25.9),
    ("ABC", 15.1),
    ("PQR", 12.7),
    ("ABC", 12.5),
    ("PQR", 10.3),
    ("IJK", 12.5),
    ("LMN", 15.6)
)

#
t_r_data = [
    ("James", "Sales", "NY", 90000, 34, 10000),
    ("Michael", "Sales", "NY", 86000, 56, 20000),
    ("Robert", "Sales", "CA", 81000, 30, 23000),
    ("Maria", "Finance", "CA", 90000, 24, 23000),
    ("Raman", "Finance", "CA", 99000, 40, 24000),
    ("Scott", "Finance", "NY", 83000, 36, 19000),
    ("Jen", "Finance", "NY", 79000, 53, 15000),
    ("Jeff", "Marketing", "CA", 80000, 25, 18000),
    ("Kumar", "Marketing", "NY", 91000, 50, 21000)
]

# Creating PairRDD student_rdd with key value pairs
t_student_marks = [
    ("Joseph", "Maths", 83),
    ("Joseph", "Physics", 74),
    ("Joseph", "Chemistry", 91),
    ("Joseph", "Biology", 82),
    ("Jimmy", "Maths", 69),
    ("Jimmy", "Physics", 62),
    ("Jimmy", "Chemistry", 97),
    ("Jimmy", "Biology", 80),
    ("Tina", "Maths", 78),
    ("Tina", "Physics", 73),
    ("Tina", "Chemistry", 68),
    ("Tina", "Biology", 87),
    ("Thomas", "Maths", 87),
    ("Thomas", "Physics", 93),
    ("Thomas", "Chemistry", 91),
    ("Thomas", "Biology", 74),
    ("Cory", "Maths", 56),
    ("Cory", "Physics", 65),
    ("Cory", "Chemistry", 71),
    ("Cory", "Biology", 68),
    ("Jackeline", "Maths", 86),
    ("Jackeline", "Physics", 62),
    ("Jackeline", "Chemistry", 75),
    ("Jackeline", "Biology", 83),
    ("Juan", "Maths", 63),
    ("Juan", "Physics", 69),
    ("Juan", "Chemistry", 64),
    ("Juan", "Biology", 60)
]

#
#
#
structureData = [
    (("James", "", "Smith"), "36636", "Sales", 34, "2006-01-01", "true", ["Java", "Scala", "C++"], {'hair': 'black', 'eye': 'brown'}, "M", 3100.50, "OH", "07-01-2019 12 01 19 406"),
    (("Michael", "Rose", ""), "40288", "Finance", 25, "2006-01-01", "true", ["Java", "Scala", "C++"], {'hair': 'brown', 'eye': 'brown'}, "M", 4300.65, "CA", "06-24-2019 12 01 19 406"),
    (("Robert", "", "Williams"), "42114", "Marketing", 27, "1992-06-23", "false", ["Java", "Scala", "C++"], {'hair': 'black', 'eye': 'black'}, "M", 1400.80, "NJ", "11-16-2019 16 50 59 406"),
    (("Maria", "Anne", "Jones"), "39192", "Finance", 19, "1987-05-05", "false", ["Java", "Scala", "C++"], {'hair': 'black', 'eye': 'brown'}, "F", 5500.75, "NY", "11-16-2019 16 50 59 406"),
    (("Jen", "Mary", "Brown"), "39191", "Marketing", 24, "1990-01-01", "false", ["Java", "Scala", "C++"], {'hair': 'black', 'eye': 'brown'}, "F", -1, "UT", "11-16-2019 16 50 59 406"),
    (("Jeff", "A", "Jones"), "39193", "Finance", 19, "2000-07-17", "false", ["Java", "Scala", "C++"], {'hair': 'black', 'eye': 'brown'}, "F", 5500.75, "CA", "11-16-2019 16 50 59 406"),
    (("Robert", "", "Williams"), "42114", "Marketing", 27, "1992-06-23", "false", ["Java", "Scala", "C++"], {'hair': 'black', 'eye': 'brown'}, "M", 1400.80, "NJ", "11-16-2019 16 50 59 406"),
    (("James", "", "Smith"), "36636", "Sales", 34, "2006-01-01", "true", ["Java", "Scala", "C++"], {'hair': 'black', 'eye': 'brown'}, "M", 3100.50, "OH", "07-01-2019 12 01 19 406"),
    (("Scott", "M", "Brown"), "39194", "Marketing", 24, "1994-10-01", "false", ["Python", "Scala", "C++"], {'hair': 'black', 'eye': 'brown'}, "F", -1, None, "11-16-2019 16 50 59 406")
]


#
#

product_revenue = [
    ("Thin",       "cell phone", 6000),
    ("Normal",     "tablet",     1500),
    ("Mini",       "tablet",     5500),
    ("Ultra thin", "cell phone", 5000),
    ("Very thin",  "cell phone", 6000),
    ("Big",        "tablet",     2500),
    ("Bendable",   "cell phone", 3000),
    ("Foldable",   "cell phone", 3000),
    ("Pro",        "tablet",     4500),
    ("Pro2",       "tablet",     6500)
]