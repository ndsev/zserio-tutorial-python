# Zserio Python Quick Start Tutorial

This Quick Start tutorial features code generation in Python. Go to the
[Zserio C++ tutorial](https://github.com/ndsev/zserio-tutorial-cpp#zserio-c-quick-start-tutorial) or
[Zserio Java tutorial](https://github.com/ndsev/zserio-tutorial-java#zserio-java-quick-start-tutorial) if you
are interested in hands-on C++ or Java with zserio.

You find the complete tutorial in this example. To follow along the description just clone this repo and check
the sources.

The latest build of the zserio compiler and runtime library can be get from
[PyPi repository](https://pypi.org/project/zserio/).

If you want to build from source, please follow the
[Zserio Compiler Build Instructions](https://github.com/ndsev/zserio/blob/master/doc/ZserioBuildInstructions.md#zserio-compiler-build-instructions).

## Installation & Prerequisites

Before we start, make sure you have the following components installed:

- Java JRE 8+
- Python 3.8+
- Zserio compiler with Python runtime library:

  ```
  python3 -m pip install zserio
  ```

## Set up dev environment

> Everything has been already set up for you in this repository. If you are very impatient, just go to the
> project's root folder and have a quick look to the schema `tutorial.zs`.
>
> Now, start to play with tutorial using the command:
>
> `python3 src/main.py`

We start with a common layout of our project/repo where we put all the source files into a `src` folder.
For simplicity the zserio schema file stays in the project's root folder.

Now we only need to generate the code, populate the `main.py` and we are done.

But before we can generate code, we need to write the schema definition of our data.

## Writing a schema

Open up your favorite text editor and start writing your schema. We will use the example from the zserio repo
plus some additional structures to showcase some of zserio's features.

```
package tutorial;

struct Employee
{
    uint8           age : age <= 65; // max age is 65
    string          name;
    uint16          salary;
    optional uint16 bonus;
    Role            role;

    // if employee is a developer, list programming skill
    Experience      skills[] if role == Role.DEVELOPER;
};

struct Experience
{
    bit:6       yearsOfExperience;
    Language    programmingLanguage;
};

enum bit:2 Language
{
    CPP     = 0,
    JAVA    = 1,
    PYTHON  = 2,
    JS      = 3
};

enum uint8 Role
{
    DEVELOPER = 0,
    TEAM_LEAD = 1,
    CTO       = 2
};
```

We have added some of zserio's features above. Let's quickly take a look:

- **Constraints**

  Although the `uint8` of field `age` would allow values up to 255, we limit the use already in the schema
  definition by using
  a [constraint](https://github.com/ndsev/zserio/blob/master/doc/ZserioLanguageOverview.md#constraints).
  If we try to write values larger than 65, the generated writers will throw an exception.

- **Optional fields**

  The `bonus` field is prefixed with the keyword `optional` which will add a invisible 1-bit bool before that
  field which indicating whether the field exists. If it is not set then only one bit will be added to the bit
  stream. See
  [Zserio Invisibles](https://github.com/ndsev/zserio/blob/master/doc/ZserioInvisibles.md#optional-keyword)
  for more information.

- **Conditions**

    We add programming skills only if the employee is developer.

- **Bit sized elements**

  The struct `Experience` uses 1 byte in total. It uses 6 bit to store the years of programming experience and
  2 bits for the enum `Language`.

For more details on the features of zserio head over to the
[Zserio Language Overview](https://github.com/ndsev/zserio/blob/master/doc/ZserioLanguageOverview.md).

We now save the file to disk as `tutorial.zs`.

> Please note that the filename has to be equivalent to the package name inside the zserio file.
> The zserio compiler accepts arbitrary file extensions (in this case `*.zs`). But make sure that all imported
> files also have the same file extension.

## Compiling and generating code

Now we are ready to compile the schema with the zserio compiler. The zserio compiler checks the schema file and
its [imported files](https://github.com/ndsev/zserio/blob/master/doc/ZserioLanguageOverview.md#packages-and-imports)
and reports errors and warnings. In addition, the zserio compiler generates code for the supported languages
and may generate HTML documentation. For a complete overview of available options, please refer to the
[Zserio Compiler User Guide](https://github.com/ndsev/zserio/blob/master/doc/ZserioUserGuide.md#zserio-compiler-user-guide).

So let's generate some Python code. It's enough just to run the following command:

```
zserio tutorial.zs -python src
```

This command generates Python code and puts it into the `src` folder. It actually creates subfolders
for each package in the schema.

So after generating the code our folder structure looks like this:

```
.
├───src
    └───tutorial
```

Let's take a quick look what has been generated. In the `src/tutorial` folder you now find the following
files:

```
api.py employee.py  experience.py __init__.py language.py role.py
```

There is a Python file for each struct or enum and a single `__init__.py` file needed to let python recognize
generated top level package as a python package.

There is also one `api.py` file for each generated package to provide a user friendly interface
to the generated api.

We now have everything ready to serialize and deserialize our data.

## Serialize using the generated code

> Note: The example code in this repository features the creation of two objects of class Employee: Joe and
> his boss. We will mostly cover the creation of Joe here.

Open up your favorite IDE and start using the zserio classes by importing the classes from the schema
and zserio runtime that we want to use.

```python
import zserio

import tutorial.api as tutorial
```

Let's declare an employee Joe and fill in some data:

```python
# declare an employee
joe = tutorial.Employee()

# fill some basic type fields
joe.age = 32
joe.name = "Joe Smith"
joe.salary = 5000

# set an enum value, in this case the role
joe.role = tutorial.Role.DEVELOPER
```

To be able to populate a list of skills, we just need to create a native python array of Experience objects.

```python
skills = [] # note that in python we use native arrays
```

So now let's generate two entries for the skills list:

First we add C++ experience:

```python
skill1 = tutorial.Experience()
skill1.years_of_experience = 8
skill1.programming_language = tutorial.Language.CPP
skills.append(skill1)
```

and then also some Python experience:

```python
# construct skill2 directly from fields
skill2 = tutorial.Experience(4, tutorial.Language.PYTHON)
skills.append(skill2)
```

Don't forget to set Joe's skills:

```python
joe.skills = skills
```

After we have set all the fields, we have to declare a BitStreamWriter and write the stream to the file:

```python
writer = zserio.BitStreamWriter()

# serialize the object joe by passing the BitStreamWriter to its write() method
joe.write(writer)

# write the buffer stored in BitStreamWriter to disk
writer.to_file(employee_file)
```

**Voila!** You have just serialized your first data with zserio.

**Congratulations!**

## Deserialize using the generated code

We already pointed out that Joe has a boss in the code we checked in. In the deserialization code we need to
keep an eye on all possible serializations we might have to deal with. So let's quickly look at the differences
between Joe and his boss.

Joe's boss is a little older, has a higher salary, gets a bonus but has no programming skills, because our
schema definition does not allow team leads to have programming skills. ;-)

```python
# set an enum value, in this case the role
boss.role = tutorial.Role.TEAM_LEAD

# no programming skills for the boss, but a bonus!
boss.bonus = 10000
```

The rest is pretty similar. Check the code to see the rest.

When deserializing the zserio bit stream, we start with reading the file using BitStreamReader declaration:

```python
reader = zserio.BitStreamReader.from_file(employee_file)
```

We declare an object of class Employee and deserialize the buffer with the help of the BitStreamReader we
just created. After this call all the fields within `employee` will be set.

```python
employee = tutorial.Employee.from_reader(reader)
```

We can now access the filled employee object via the respective getters. We still need to check for optionals
and conditionals whether they have been set.

```python
# data types that are always available can simply be printed out
print("Name:", employee.name)
print("Age:", employee.age)
print("Salary:", employee.salary)
print("Role:", employee.role)

# we have to check for optionals whether they are in the stream
if employee.is_bonus_used():
    print("Bonus:", employee.bonus)
```

For the rest of the processing please refer to the code. You should have gotten the main point by now.

## Additions you will find in the code

There are some other features that we used in the code in this repo that we would like to point out briefly:

- zserio runtime exception handling
- some zserio API calls

### Zserio runtime exceptions

The zserio runtime throws the `zserio.PythonRuntimeException` and possibly other python built-in 
exceptions e.g. when a file is missing or when wrong arguments are passed to a function.

It makes sense to try-except all of your writes and reads as we do in our tutorial:

```python
try:
    # read or write
except zserio.PythonRuntimeException as excpt:
    print("Zserio error:", excpt)
except Exception as excpt:
    print("Error:", excpt)
```

Example for when PythonRuntimeException will be thrown:

- **Constraint exceptions**

  If there is a constrain in the schema that requires a certain field to be set to specific value, the
  zserio runtime will throw an exception if you try to set the field without the constraint being met.

  > Example: Try to make Joe 100 years old.

### Zserio API calls

The example uses one smaller feature that we would like to explain.

The feature is that you can always retrieve the actual bit size of the structures in zserio by calling
`bitsizeof()`.

In the tutorial we use it for plain informational purpose only.

```python
print("Bit size of employee: ", employee.bitsizeof())
```
