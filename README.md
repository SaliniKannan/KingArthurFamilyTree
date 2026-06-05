**King Arthur Family Tree**

**Overview**

This application models the King Arthur family tree and supports:

1. Adding a child to a family.


2. Finding relationships between family members.


3. Processing commands from an input file.


4. Printing results to the console.



The solution is implemented using an object-oriented approach where each person is represented as a object and relationships are represented through object references.


---

**Design Approach**

**Person Model**

Each person in the family tree contains:

name
gender
mother
father
spouse
children

This structure allows efficient traversal of the family tree in all directions.

**Family Tree Structure**

The family tree is maintained as a collection of Person objects stored in a dictionary:

people = {
    person_name: Person
}

This provides O(1) lookup for relationship queries.


---

**Supported Commands**

Add Child

Input:

ADD_CHILD <MotherName> <ChildName> <Gender>

Example:

ADD_CHILD Flora Minerva Female

Output:

CHILD_ADDED

Validation:

Mother must exist.

Mother must be female.

---

**Get Relationship**

Input:

GET_RELATIONSHIP <PersonName> <Relationship>

Example:

GET_RELATIONSHIP molly Siblings

Output:

lucy


---

**Relationships Supported**

The solution supports:

Mother

Father

Son

Daughter

Siblings

Brother-In-Law

Sister-In-Law

Maternal Aunt

Maternal Uncle

Paternal Aunt

Paternal Uncle


Additional relationships can be added easily.


---

**Relationship Resolution Logic**

**Siblings**

People sharing the same mother.

**Maternal Aunt**

Female siblings of the person's mother.

**Maternal Uncle**

Male siblings of the person's mother.

**Paternal Aunt**

Female siblings of the person's father.

**Paternal Uncle**

Male siblings of the person's father.

**Sister-In-Law**

Obtained through:

Spouse's sisters

Wives of person's brothers


**Brother-In-Law**

Obtained through:

Spouse's brothers

Husbands of person's sisters



---

**Error Handling**

**Person Not Found**

Output:

PERSON_NOT_FOUND

**Child Addition Failed**

Output:

CHILD_ADDITION_FAILED

**Relationship Not Found**

Output:

NONE

---
---

**Family Tree Initialization**
The initial King Arthur family tree is maintained in a separate file named king_arthur_family.txt.
When the application starts, it reads and parses this file to construct the family tree dynamically. Each family member is represented as a Person object containing information such as name, gender, parents, spouse, and children.

**The application establishes:**
Parent-child relationships
Spouse relationships
Family hierarchy
Storing the family data in a separate file keeps the family structure independent of the application logic, making the solution easier to maintain and extend.

**Execution Instructions**
**Prerequisites**
Python 3.x installed on the system.

**Running the Application**
Execute the application using:
Bash
python main.py

**Application Flow**
The application loads the initial family data from king_arthur_family.txt.
The family tree is constructed in memory.
The user is prompted to enter commands.
The application processes the commands and displays the corresponding output.

**Sample Input**

ADD_CHILD Flora Minerva Female
GET_RELATIONSHIP Minerva Paternal-Uncle
GET_RELATIONSHIP moly Siblings

Sample Output

CHILD_ADDED
Victorie
lucy


---

**Assumptions**

Every child has one mother and one father.

Spouse relationships are bidirectional.

Family members are uniquely identified by name.

Relationship lookups are case-sensitive.
