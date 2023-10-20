"""
Zserio Python tutorial.
"""

import sys

import zserio

import tutorial.api as tutorial

def _print_help():
    print("Usage: main.py write_joe|write_boss|read")

def _write_joe(employee_file: str):
    # create an employee
    joe = tutorial.Employee()

    # fill some basic type fields
    joe.age = 32
    joe.name = "Joe Smith"
    joe.salary = 5000

    # set an enum value, in this case the role
    joe.role = tutorial.Role.DEVELOPER

    # add skills
    skills = [] # note that in python we use native arrays

    skill1 = tutorial.Experience()
    skill1.years_of_experience = 8
    skill1.programming_language = tutorial.Language.CPP
    skills.append(skill1)

    # construct skill2 directly from fields
    skill2 = tutorial.Experience(4, tutorial.Language.PYTHON)
    skills.append(skill2)

    joe.skills = skills

    # create new BitStreamWriter
    writer = zserio.BitStreamWriter()

    # serialize the object joe by passing the BitStreamWriter to its write() method
    joe.write(writer)

    # write the buffer stored in BitStreamWriter to disk
    writer.to_file(employee_file)

def _write_boss(employee_file: str):
    # create an employee
    boss = tutorial.Employee()

    # fill some basic fields
    boss.age = 43
    boss.name = "Boss"
    boss.salary = 9000

    # set an enum value, in this case the role
    boss.role = tutorial.Role.TEAM_LEAD

    # no programming skills for the boss, but a bonus!
    boss.bonus = 10000

    # create new BitStreamWriter
    writer = zserio.BitStreamWriter()

    # serialize the object boss by passing the BitStreamWriter to its write() method
    boss.write(writer)

    # write the buffer stored in the BitStreamWriter to disk
    writer.to_file(employee_file)

def _read_employee(employee_file: str):
    # create new BitStreamReader using the file to read from
    reader = zserio.BitStreamReader.from_file(employee_file)

    # deserialize the stream to an Employee class
    employee = tutorial.Employee.from_reader(reader)

    # data types that are always available can simply be printed out
    print("Name:", employee.name)
    print("Age:", employee.age)
    print("Salary:", employee.salary)
    print("Role:", employee.role)

    # we have to check for optionals whether they are in the stream
    if employee.is_bonus_used():
        print("Bonus:", employee.bonus)

    # we also have to check for conditions if they applied
    if employee.is_skills_used():
        for skill in employee.skills:
            years = skill.years_of_experience
            language = skill.programming_language
            print(f"Skill: Language {language}, {years} years")

    # print out bit size
    print("Bit size of employee: ", employee.bitsizeof())

def _main() -> int:
    if len(sys.argv) != 2:
        _print_help()
        return 2

    employee_file = "employee.zsb"

    try:
        if sys.argv[1] == "write_joe":
            _write_joe(employee_file)
        elif sys.argv[1] == "write_boss":
            _write_boss(employee_file)
        elif sys.argv[1] == "read":
            _read_employee(employee_file)
        else:
            _print_help()
            if sys.argv[1] != "-h" and sys.argv[1] != "--help":
                return 2
    except zserio.PythonRuntimeException as excpt:
        print("Zserio error:", excpt)
        return 1
    except Exception as excpt:
        print("Error:", excpt)
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(_main())
