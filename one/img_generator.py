"""PNG student card generator - Penn State LionPATH (randomized)"""
import random
from datetime import datetime
from io import BytesIO


def generate_psu_id():
    """Generate random PSU ID (9 digits)"""
    return f"9{random.randint(10000000, 99999999)}"


def generate_psu_email(first_name, last_name):
    """Generate PSU email: firstName.lastName + 3-4 digits @psu.edu"""
    digit_count = random.choice([3, 4])
    digits = ''.join([str(random.randint(0, 9)) for _ in range(digit_count)])
    email = f"{first_name.lower()}.{last_name.lower()}{digits}@psu.edu"
    return email


# ============================================================
# Randomized course data
# ============================================================

COURSES_POOL = [
    # (code, title, units)
    ("CMPSC 121", "Introduction to Programming", "3.00"),
    ("CMPSC 122", "Intermediate Programming", "3.00"),
    ("CMPSC 131", "Programming and Computation I", "3.00"),
    ("CMPSC 132", "Programming and Computation II", "3.00"),
    ("CMPSC 221", "Object-Oriented Programming with Web", "3.00"),
    ("CMPSC 360", "Discrete Mathematics for CS", "3.00"),
    ("CMPSC 431W", "Database Management Systems", "3.00"),
    ("CMPSC 461", "Programming Language Concepts", "3.00"),
    ("CMPSC 465", "Data Structures and Algorithms", "3.00"),
    ("CMPSC 473", "Operating Systems Design", "3.00"),
    ("CMPSC 474", "Server-Side Web Development", "3.00"),
    ("CMPSC 483W", "Software Engineering Capstone", "3.00"),
    ("MATH 140", "Calculus With Analytic Geometry I", "4.00"),
    ("MATH 141", "Calculus With Analytic Geometry II", "4.00"),
    ("MATH 220", "Matrices", "2.00"),
    ("MATH 230", "Calculus and Vector Analysis", "4.00"),
    ("MATH 231", "Calculus of Several Variables", "2.00"),
    ("MATH 251", "Ordinary and Partial Differential Equations", "4.00"),
    ("MATH 311W", "Concepts of Discrete Mathematics", "3.00"),
    ("STAT 200", "Elementary Statistics", "4.00"),
    ("STAT 318", "Elementary Probability", "3.00"),
    ("STAT 414", "Introduction to Probability Theory", "3.00"),
    ("PHYS 211", "General Physics: Mechanics", "4.00"),
    ("PHYS 212", "General Physics: Electricity and Magnetism", "4.00"),
    ("PHYS 213", "Foundations of Physics III", "2.00"),
    ("ENGL 015", "Rhetoric and Composition", "3.00"),
    ("ENGL 202C", "Technical Writing", "3.00"),
    ("ENGL 030", "Heritage of Western Literature", "3.00"),
    ("ECON 102", "Introductory Microeconomic Analysis", "3.00"),
    ("ECON 104", "Introductory Macroeconomic Analysis", "3.00"),
    ("IST 110", "Information, People, and Technology", "3.00"),
    ("IST 210", "Organization of Data", "3.00"),
    ("IST 261", "Application Development Design", "3.00"),
    ("IST 311", "Object-Oriented Design and Software Applications", "3.00"),
    ("PSYCH 100", "Introductory Psychology", "3.00"),
    ("COMM 150", "Effective Speech", "3.00"),
    ("BIOL 110", "Biology: Basic Concepts and Biodiversity", "4.00"),
    ("CHEM 110", "Chemical Principles I", "3.00"),
    ("SOC 119", "Introduction to Sociology", "3.00"),
    ("HIST 020", "American Civilization to 1877", "3.00"),
    ("PHIL 103", "Introduction to Ethics", "3.00"),
    ("ACCTG 211", "Financial and Managerial Accounting", "4.00"),
    ("MGMT 301", "Basic Management Concepts", "3.00"),
    ("MKTG 301", "Principles of Marketing", "3.00"),
    ("FIN 301", "Corporation Finance", "3.00"),
    ("EE 210", "Circuits and Devices", "4.00"),
    ("ME 201", "Introduction to Thermodynamics", "3.00"),
    ("KINES 084", "Concepts of Fitness and Wellness", "3.00"),
]

ROOMS_POOL = [
    # (building, room_number)
    ("Willard", ["062", "119", "203", "315"]),
    ("Thomas", ["102", "201", "310", "117"]),
    ("Westgate", ["E101", "E201", "W103", "W210"]),
    ("Boucke", ["210", "304", "106", "225"]),
    ("Osmond", ["112", "215", "101", "306"]),
    ("Hammond", ["100", "218", "312", "114"]),
    ("Deike", ["115", "207", "308", "104"]),
    ("Sackett", ["201", "302", "110", "204"]),
    ("Sparks", ["101", "203", "315", "106"]),
    ("Rackley", ["102", "204", "301", "105"]),
    ("IST", ["120", "220", "325", "118"]),
    ("Smeal", ["106", "210", "314", "100"]),
    ("Forum", ["101", "207", "301", "114"]),
    ("Kern", ["103", "212", "314", "107"]),
    ("Wartik", ["100", "111", "222", "300"]),
    ("Mueller", ["103", "204", "301", "105"]),
    ("Henderson", ["101", "204", "308", "112"]),
    ("Leonhard", ["100", "203", "307", "115"]),
]

TIME_SLOTS = [
    "MoWeFr 8:00AM - 8:50AM",
    "MoWeFr 9:05AM - 9:55AM",
    "MoWeFr 10:10AM - 11:00AM",
    "MoWeFr 11:15AM - 12:05PM",
    "MoWeFr 1:25PM - 2:15PM",
    "MoWeFr 2:30PM - 3:20PM",
    "MoWeFr 3:35PM - 4:25PM",
    "TuTh 8:00AM - 9:15AM",
    "TuTh 9:05AM - 10:20AM",
    "TuTh 10:35AM - 11:50AM",
    "TuTh 12:05PM - 1:20PM",
    "TuTh 1:35PM - 2:50PM",
    "TuTh 2:30PM - 3:45PM",
    "TuTh 4:00PM - 5:15PM",
    "Mo 6:00PM - 8:50PM",
    "Tu 6:00PM - 8:50PM",
    "We 6:00PM - 8:50PM",
    "Th 6:00PM - 8:50PM",
]

MAJORS = [
    "Computer Science (BS)",
    "Software Engineering (BS)",
    "Information Sciences and Technology (BS)",
    "Data Science (BS)",
    "Electrical Engineering (BS)",
    "Mechanical Engineering (BS)",
    "Business Administration (BS)",
    "Psychology (BA)",
    "Biology (BS)",
    "Chemistry (BS)",
    "Mathematics (BS)",
    "Economics (BA)",
    "Communications (BA)",
    "Accounting (BS)",
    "Finance (BS)",
    "Marketing (BS)",
    "Civil Engineering (BS)",
    "Aerospace Engineering (BS)",
]


def _get_current_semester():
    """Return the current semester string based on today's date."""
    now = datetime.now()
    month = now.month
    year = now.year

    if month >= 8:
        return f"Fall {year}", f"Aug 25 - Dec 12"
    elif month >= 5:
        return f"Summer {year}", f"May 13 - Aug 8"
    else:
        return f"Spring {year}", f"Jan 13 - May 2"


def _generate_random_schedule():
    """Generate 4-5 random courses with unique times and rooms."""
    num_courses = random.choice([4, 5])
    courses = random.sample(COURSES_POOL, num_courses)
    times = random.sample(TIME_SLOTS, num_courses)

    schedule = []
    for i, (code, title, units) in enumerate(courses):
        building = random.choice(ROOMS_POOL)
        room = f"{building[0]} {random.choice(building[1])}"
        class_nbr = str(random.randint(10000, 29999))
        schedule.append({
            "class_nbr": class_nbr,
            "code": code,
            "title": title,
            "time": times[i],
            "room": room,
            "units": units,
        })

    return schedule


def generate_html(first_name, last_name, school_id='2565'):
    """Generate Penn State LionPATH HTML with randomized data.

    Args:
        first_name: First name
        last_name: Last name
        school_id: School ID

    Returns:
        str: HTML content
    """
    psu_id = generate_psu_id()
    name = f"{first_name} {last_name}"
    date = datetime.now().strftime('%m/%d/%Y, %I:%M:%S %p')
    major = random.choice(MAJORS)
    semester, semester_range = _get_current_semester()
    schedule = _generate_random_schedule()

    # Build course rows
    course_rows = ""
    for c in schedule:
        course_rows += f"""
                <tr>
                    <td>{c['class_nbr']}</td>
                    <td class="course-code">{c['code']}</td>
                    <td class="course-title">{c['title']}</td>
                    <td>{c['time']}</td>
                    <td>{c['room']}</td>
                    <td>{c['units']}</td>
                </tr>"""

    # Calculate total units
    total_units = sum(float(c['units']) for c in schedule)

    # Current year for copyright
    current_year = datetime.now().year

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LionPATH - Student Home</title>
    <style>
        :root {{
            --psu-blue: #1E407C;
            --psu-light-blue: #96BEE6;
            --bg-gray: #f4f4f4;
            --text-color: #333;
        }}

        body {{
            font-family: "Roboto", "Helvetica Neue", Helvetica, Arial, sans-serif;
            background-color: #e0e0e0;
            margin: 0;
            padding: 20px;
            color: var(--text-color);
            display: flex;
            justify-content: center;
        }}

        .viewport {{
            width: 100%;
            max-width: 1100px;
            background-color: #fff;
            box-shadow: 0 5px 20px rgba(0,0,0,0.15);
            min-height: 800px;
            display: flex;
            flex-direction: column;
        }}

        .header {{
            background-color: var(--psu-blue);
            color: white;
            padding: 0 20px;
            height: 60px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}

        .brand {{
            display: flex;
            align-items: center;
            gap: 15px;
        }}

        .psu-logo {{
            font-family: "Georgia", serif;
            font-size: 20px;
            font-weight: bold;
            letter-spacing: 1px;
            border-right: 1px solid rgba(255,255,255,0.3);
            padding-right: 15px;
        }}

        .system-name {{
            font-size: 18px;
            font-weight: 300;
        }}

        .user-menu {{
            font-size: 14px;
            display: flex;
            align-items: center;
            gap: 20px;
        }}

        .nav-bar {{
            background-color: #f8f8f8;
            border-bottom: 1px solid #ddd;
            padding: 10px 20px;
            font-size: 13px;
            color: #666;
            display: flex;
            gap: 20px;
        }}
        .nav-item {{ cursor: pointer; }}
        .nav-item.active {{ color: var(--psu-blue); font-weight: bold; border-bottom: 2px solid var(--psu-blue); padding-bottom: 8px; }}

        .content {{
            padding: 30px;
            flex: 1;
        }}

        .page-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
            margin-bottom: 20px;
            border-bottom: 1px solid #eee;
            padding-bottom: 10px;
        }}

        .page-title {{
            font-size: 24px;
            color: var(--psu-blue);
            margin: 0;
        }}

        .term-selector {{
            background: #fff;
            border: 1px solid #ccc;
            padding: 5px 10px;
            border-radius: 4px;
            font-size: 14px;
            color: #333;
            font-weight: bold;
        }}

        .student-card {{
            background: #fcfcfc;
            border: 1px solid #e0e0e0;
            padding: 15px;
            margin-bottom: 25px;
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
            font-size: 13px;
        }}
        .info-label {{ color: #777; font-size: 11px; text-transform: uppercase; margin-bottom: 4px; }}
        .info-val {{ font-weight: bold; color: #333; font-size: 14px; }}
        .status-badge {{
            background-color: #e6fffa; color: #007a5e;
            padding: 4px 8px; border-radius: 4px; font-weight: bold; border: 1px solid #b2f5ea;
        }}

        .schedule-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
        }}

        .schedule-table th {{
            text-align: left;
            padding: 12px;
            background-color: #f0f0f0;
            border-bottom: 2px solid #ccc;
            color: #555;
        }}

        .schedule-table td {{
            padding: 15px 12px;
            border-bottom: 1px solid #eee;
        }}

        .course-code {{ font-weight: bold; color: var(--psu-blue); }}
        .course-title {{ font-weight: 500; }}

        .total-row {{
            font-weight: bold;
            background-color: #f8f8f8;
        }}

        @media print {{
            body {{ background: white; padding: 0; }}
            .viewport {{ box-shadow: none; max-width: 100%; min-height: auto; }}
            .nav-bar {{ display: none; }}
            @page {{ margin: 1cm; size: landscape; }}
        }}
    </style>
</head>
<body>

<div class="viewport">
    <div class="header">
        <div class="brand">
            <div class="psu-logo">PennState</div>
            <div class="system-name">LionPATH</div>
        </div>
        <div class="user-menu">
            <span>Welcome, <strong>{name}</strong></span>
            <span>|</span>
            <span>Sign Out</span>
        </div>
    </div>

    <div class="nav-bar">
        <div class="nav-item">Student Home</div>
        <div class="nav-item active">My Class Schedule</div>
        <div class="nav-item">Academics</div>
        <div class="nav-item">Finances</div>
        <div class="nav-item">Campus Life</div>
    </div>

    <div class="content">
        <div class="page-header">
            <h1 class="page-title">My Class Schedule</h1>
            <div class="term-selector">
                Term: <strong>{semester}</strong> ({semester_range})
            </div>
        </div>

        <div class="student-card">
            <div>
                <div class="info-label">Student Name</div>
                <div class="info-val">{name}</div>
            </div>
            <div>
                <div class="info-label">PSU ID</div>
                <div class="info-val">{psu_id}</div>
            </div>
            <div>
                <div class="info-label">Academic Program</div>
                <div class="info-val">{major}</div>
            </div>
            <div>
                <div class="info-label">Enrollment Status</div>
                <div class="status-badge">&#10003; Enrolled</div>
            </div>
        </div>

        <div style="margin-bottom: 10px; font-size: 12px; color: #666; text-align: right;">
            Data retrieved: <span>{date}</span>
        </div>

        <table class="schedule-table">
            <thead>
                <tr>
                    <th width="10%">Class Nbr</th>
                    <th width="15%">Course</th>
                    <th width="35%">Title</th>
                    <th width="20%">Days &amp; Times</th>
                    <th width="10%">Room</th>
                    <th width="10%">Units</th>
                </tr>
            </thead>
            <tbody>{course_rows}
                <tr class="total-row">
                    <td colspan="5" style="text-align: right;">Total Units:</td>
                    <td>{total_units:.2f}</td>
                </tr>
            </tbody>
        </table>

        <div style="margin-top: 50px; border-top: 1px solid #ddd; padding-top: 10px; font-size: 11px; color: #888; text-align: center;">
            &copy; {current_year} The Pennsylvania State University. All rights reserved.<br>
            LionPATH is the student information system for Penn State.
        </div>
    </div>
</div>

</body>
</html>
"""

    return html


def generate_image(first_name, last_name, school_id='2565'):
    """Generate Penn State LionPATH screenshot PNG.

    Args:
        first_name: First name
        last_name: Last name
        school_id: School ID

    Returns:
        bytes: PNG image data
    """
    try:
        from playwright.sync_api import sync_playwright

        html_content = generate_html(first_name, last_name, school_id)

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={'width': 1200, 'height': 900})
            page.set_content(html_content, wait_until='load')
            page.wait_for_timeout(500)
            screenshot_bytes = page.screenshot(type='png', full_page=True)
            browser.close()

        return screenshot_bytes

    except ImportError:
        raise Exception("Playwright required: pip install playwright && playwright install chromium")
    except Exception as e:
        raise Exception(f"Image generation failed: {str(e)}")


if __name__ == '__main__':
    import sys
    import io

    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    print("Testing PSU image generation...")

    first_name = "John"
    last_name = "Smith"

    print(f"Name: {first_name} {last_name}")
    print(f"PSU ID: {generate_psu_id()}")
    print(f"Email: {generate_psu_email(first_name, last_name)}")

    try:
        img_data = generate_image(first_name, last_name)
        with open('test_psu_card.png', 'wb') as f:
            f.write(img_data)
        print(f"OK! Image size: {len(img_data)} bytes")
        print("Saved as test_psu_card.png")
    except Exception as e:
        print(f"Error: {e}")
