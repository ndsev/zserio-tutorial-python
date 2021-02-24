#!/usr/bin/env python3
"""
Zserio Python tutorial.
"""

import os
import sys
MIN_PYTHON = (3, 8)
if sys.version_info < MIN_PYTHON:
    sys.exit("Python %s.%s or later is required.\n" % MIN_PYTHON)

# add path to zserio runtime
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "3rdparty", "runtime"))
# add src to path
sys.path.append(os.path.dirname(__file__))

import zserio
import tutorial.api as tutorial

def _printHelp():
    print("Usage: Main.py write_joe|write_boss|read")

def _writeJoe(employeeFile):
    # create an employee
    joe = tutorial.Employee()

    # fill some basic type fields
    joe.setAge(32)
    joe.setName("Joe Smith")
    joe.setSalary(5000)

    # set an enum value, in this case the role
    joe.setRole(tutorial.Role.DEVELOPER)

    # add skills
    skills = [] # note that in python we use native arrays

    skill1 = tutorial.Experience()
    skill1.setYearsOfExperience(8)
    skill1.setProgrammingLanguage(tutorial.Language.CPP)
    skills.append(skill1)

    # construct skill2 directly from fields
    skill2 = tutorial.Experience(4, tutorial.Language.PYTHON)
    skills.append(skill2)

    joe.setSkills(skills)

    # create new BitStreamWriter
    writer = zserio.BitStreamWriter()

    # serialize the object joe by passing the BitStreamWriter to its write() method
    joe.write(writer)

    # write the buffer stored in BitStreamWriter to disk
    writer.toFile(employeeFile)

def _writeBoss(employeeFile):
    # create an employee
    boss = tutorial.Employee()

    # fill some basic fields
    boss.setAge(43)
    boss.setName("Boss")
    boss.setSalary(9000)

    # set an enum value, in this case the role
    boss.setRole(tutorial.Role.TEAM_LEAD)

    # no programming skills for the boss, but a bonus!
    boss.setBonus(10000)

    # create new BitStreamWriter
    writer = zserio.BitStreamWriter()

    # serialize the object boss by passing the BitStreamWriter to its write() method
    boss.write(writer)

    # write the buffer stored in the BitStreamWriter to disk
    writer.toFile(employeeFile)

def _readEmployee(employeeFile):
    # create new BitStreamReader using the file to read from
    reader = zserio.BitStreamReader.fromFile(employeeFile)

    # deserialize the stream to an Employee class
    employee = tutorial.Employee.fromReader(reader)

    # data types that are always available can simply be printed out
    print("Name:", employee.getName())
    print("Age:", employee.getAge())
    print("Salary:", employee.getSalary())
    print("Role:", employee.getRole())

    # we have to check for optionals whether they are in the stream
    if employee.isBonusUsed():
        print("Bonus:", employee.getBonus())

    # we also have to check for conditions if they applied
    if employee.isSkillsUsed():
        for skill in employee.getSkills():
            years = skill.getYearsOfExperience()
            language = skill.getProgrammingLanguage()
            print("Skill: Language {}, {} years".format(language, years))

    # print out bit size
    print("Bit size of employee: ", employee.bitSizeOf())

if __name__ == "__main__":
    if len(sys.argv) != 2:
        _printHelp()
        sys.exit(2)

    employeeFile = "employee.zsb"

    try:
        if sys.argv[1] == "write_joe":
            _writeJoe(employeeFile)
        elif sys.argv[1] == "write_boss":
            _writeBoss(employeeFile)
        elif sys.argv[1] == "read":
            _readEmployee(employeeFile)
        else:
            _printHelp()
            if sys.argv[1] != "-h" and sys.argv[1] != "--help":
                sys.exit(2)
    except zserio.PythonRuntimeException as e:
        print("Zserio error:", e)
        sys.exit(1)
    except Exception as e:
        print("Error:", e)
        sys.exit(1)
