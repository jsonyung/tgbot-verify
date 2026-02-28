"""
Generates realistic American names to improve success rate and avoid fraud detection.
"""
import random
from datetime import datetime, timedelta

class NameGenerator:
    """
    Generates a random, realistic American name from expanded lists.
    This helps avoid pattern detection by SheerID's fraud systems.
    """
    # SOLUTION: Massively expanded the name lists to create thousands more unique combinations,
    # reducing the chance of submitting a name that has been flagged before.
    first_names = [
        # Common Male Names
        "James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph",
        "Thomas", "Charles", "Christopher", "Daniel", "Matthew", "Anthony", "Mark",
        "Donald", "Steven", "Paul", "Andrew", "Joshua", "Kenneth", "Kevin", "Brian",
        "George", "Edward", "Ronald", "Timothy", "Jason", "Jeffrey", "Ryan", "Jacob",
        "Gary", "Nicholas", "Eric", "Jonathan", "Stephen", "Larry", "Justin", "Scott",
        "Brandon", "Benjamin", "Samuel", "Gregory", "Frank", "Alexander", "Raymond",
        "Patrick", "Jack", "Dennis", "Jerry", "Tyler", "Aaron", "Jose", "Adam", "Henry",
        "Nathan", "Douglas", "Zachary", "Peter", "Kyle", "Walter", "Ethan", "Jeremy",
        "Harold", "Keith", "Christian", "Roger", "Noah", "Gerald", "Carl", "Terry",
        "Sean", "Austin", "Arthur", "Lawrence", "Jesse", "Dylan", "Bryan", "Joe",
        "Jordan", "Billy", "Bruce", "Albert", "Willie", "Gabriel", "Logan", "Alan",
        "Juan", "Wayne", "Roy", "Ralph", "Randy", "Eugene", "Vincent", "Russell",
        "Elijah", "Louis", "Bobby", "Philip", "Johnny", "Caleb", "Isaac", "Mason",

        # Common Female Names
        "Mary", "Patricia", "Jennifer", "Linda", "Elizabeth", "Barbara", "Susan",
        "Jessica", "Sarah", "Karen", "Nancy", "Lisa", "Betty", "Margaret", "Sandra",
        "Ashley", "Kimberly", "Emily", "Donna", "Michelle", "Dorothy", "Carol",
        "Amanda", "Melissa", "Deborah", "Stephanie", "Rebecca", "Sharon", "Laura",
        "Cynthia", "Kathleen", "Amy", "Shirley", "Angela", "Helen", "Anna", "Brenda",
        "Pamela", "Nicole", "Emma", "Samantha", "Katherine", "Christine", "Debra",
        "Rachel", "Catherine", "Carolyn", "Janet", "Ruth", "Maria", "Heather",
        "Diane", "Virginia", "Julie", "Joyce", "Victoria", "Olivia", "Kelly",
        "Christina", "Lauren", "Joan", "Evelyn", "Judith", "Megan", "Cheryl",
        "Andrea", "Hannah", "Martha", "Jacqueline", "Frances", "Gloria", "Ann",
        "Teresa", "Kathryn", "Sara", "Janice", "Jean", "Alice", "Madison",
        "Doris", "Rose", "Isabella", "Amber", "Marilyn", "Danielle",
        "Brittany", "Diana", "Natalie", "Sophia", "Grace", "Lily", "Chloe"
    ]
    last_names = [
        "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
        "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
        "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson",
        "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker",
        "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill",
        "Flores", "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell",
        "Mitchell", "Carter", "Roberts", "Gomez", "Phillips", "Evans", "Turner",
        "Diaz", "Parker", "Cruz", "Edwards", "Collins", "Reyes", "Stewart", "Morris",
        "Morales", "Murphy", "Cook", "Rogers", "Gutierrez", "Ortiz", "Morgan",
        "Cooper", "Peterson", "Bailey", "Reed", "Kelly", "Howard", "Ramos", "Kim",
        "Cox", "Ward", "Richardson", "Watson", "Brooks", "Chavez", "Wood", "James",
        "Bennet", "Gray", "Mendoza", "Ruiz", "Hughes", "Price", "Alvarez", "Castillo",
        "Sanders", "Patel", "Myers", "Long", "Ross", "Foster", "Jimenez", "Powell",
        "Jenkins", "Perry", "Russell", "Sullivan", "Bell", "Coleman", "Butler",
        "Henderson", "Barnes", "Gonzales", "Fisher", "Vasquez", "Simmons", "Graham",
        "Murray", "Ford", "Castro", "Marshall", "Owens", "Harrison", "Fernandez",
        "McDonald", "Woods", "Washington", "Kennedy", "Wells", "Vargas", "Henry",
        "Chen", "Freeman", "Webb", "Tucker", "Hicks", "Crawford", "Cunningham",
        "Watkins", "Harper", "Schmidt", "Shaw", "Murray", "Ford", "Hamilton"
    ]

    @staticmethod
    def generate():
        """Generates a dictionary containing a random first and last name."""
        first_name = random.choice(NameGenerator.first_names)
        last_name = random.choice(NameGenerator.last_names)
        return {"first_name": first_name, "last_name": last_name}

def generate_birth_date(min_age=19, max_age=25):
    """
    Generates a random birth date for a typical college-aged student.
    Returns a date string in YYYY-MM-DD format.
    """
    today = datetime.today()
    start_date = today - timedelta(days=max_age * 365)
    end_date = today - timedelta(days=min_age * 365)
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    birth_date = start_date + timedelta(days=random_number_of_days)
    return birth_date.strftime("%Y-%m-%d")
