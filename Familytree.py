#!/usr/bin/env python
# coding: utf-8

# In[ ]:


class Person:
    """
    Represents an individual within the family tree.
    Tracks relationships such as parents, spouse, and children.
    """
    def __init__(self, name, gender):
        self.name = name.lower()
        self.gender = gender.lower()
        self.mother = None
        self.father = None
        self.spouse = None
        self.children = [] 
        print(f"{self.name} initialised")
        
    def ADD_CHILD(self, child_name, child_gender, family):
        """
        Adds a child to the family tree if the current person is female.
        Automatically links the child to the father if a spouse exists.
        """
        # Children can only be added through the mother
        if self.gender == 'female':
            # Check if this specific mother already has a child with this name
            # We look at the names of the children currently in self.children
            existing_child_names = [child.name for child in self.children]
            if child_name in existing_child_names:
                print('CHILD_ALREADY_EXISTS')
                return
            child = Person(child_name, child_gender)
            family[child_name] = child
        
            # Establish maternal links
            child.mother = self
            self.children.append(child) 
            
            # Establish paternal links if a father (spouse) exists
            if self.spouse:
                child.father = self.spouse
                self.spouse.children.append(child) 
            print('CHILD_ADDITION_SUCCEDED')
        else:
            print('CHILD_ADDITION_FAILED')
            
    def GET_RELATIONSHIP(self, relationship):
        """
        Dynamically fetches relationships either via built-in attributes 
        or by routing to dedicated helper functions.
        """
        # Check if the relationship maps directly to an attribute (e.g., mother, spouse)
        if hasattr(self, relationship):
            relationship_obj = getattr(self, relationship)
            
            if isinstance(relationship_obj, list):
                return [child.name for child in relationship_obj]
            elif relationship_obj is not None:
                return [relationship_obj.name]
            return []
        
        # Route complex relationship queries to helper methods
        else:
            all_relationships = {
                "son": self.get_son,
                "sons": self.get_son,
                "daughter": self.get_daughter,
                "daughters": self.get_daughter,
                "sibling": self.get_sibling,
                "siblings": self.get_sibling,
                "paternal-uncle": self.get_paternal_uncle,
                "maternal-uncle": self.get_maternal_uncle,
                "paternal-aunt": self.get_paternal_aunt,
                "maternal-aunt": self.get_maternal_aunt,
                "sister-in-law": self.get_sisterinlaw,
                "brother-in-law": self.get_brotherinlaw
            }
        
            if relationship in all_relationships:
                return all_relationships[relationship]()
            else:
                print("INVALID_RELATIONSHIP")
                return []
            
    def get_paternal_uncle(self):
        """Returns a list of brothers belonging to the person's father."""
        if self.father:
            return [sib_name for sib_name in self.father.get_sibling() if family[sib_name].gender == 'male']
        return []
    
    def get_maternal_uncle(self):
        """Returns a list of brothers belonging to the person's mother."""
        if self.mother:
            return [sib_name for sib_name in self.mother.get_sibling() if family[sib_name].gender == 'male']   
        return []
    
    def get_paternal_aunt(self):
        """Returns a list of sisters belonging to the person's father."""
        if self.father:
            return [sib_name for sib_name in self.father.get_sibling() if family[sib_name].gender == 'female'] 
        return []
        
    def get_maternal_aunt(self):
        """Returns a list of sisters belonging to the person's mother."""
        if self.mother:
            return [sib_name for sib_name in self.mother.get_sibling() if family[sib_name].gender == 'female']   
        return []
        
    def get_sisterinlaw(self):
        """Returns a list of spouse's sisters and brothers' wives."""
        results = []
        
        # 1. Look for Spouse's sisters
        if self.spouse:
            for sib_name in self.spouse.get_sibling():
                sibling_obj = family[sib_name]
                if sibling_obj.gender == 'female':
                    results.append(sibling_obj.name)
                    
        # 2. Look for Wives of siblings
        for sib_name in self.get_sibling():
            sibling_obj = family[sib_name]
            if sibling_obj.gender == 'male' and sibling_obj.spouse:
                results.append(sibling_obj.spouse.name)
        return results
               
    def get_brotherinlaw(self):
        """Returns a list of spouse's brothers and sisters' husbands."""
        results = []
        
        # 1. Look for Spouse's brothers
        if self.spouse:
            for sib_name in self.spouse.get_sibling():
                sibling_obj = family[sib_name]
                if sibling_obj.gender == 'male':
                    results.append(sibling_obj.name)
                    
        # 2. Look for Husbands of siblings
        for sib_name in self.get_sibling():
            sibling_obj = family[sib_name]
            if sibling_obj.gender == 'female' and sibling_obj.spouse:
                results.append(sibling_obj.spouse.name)
        return results
        
    def get_son(self):
        """Filters children to return only males."""
        return [child.name for child in self.children if child.gender == 'male']
    
    def get_daughter(self):
        """Filters children to return only females."""
        return [child.name for child in self.children if child.gender == 'female']
    
    def get_sibling(self):
        """Returns all other children sharing the same mother."""
        if self.mother:
            return [child.name for child in self.mother.children if child != self]
        return []


def create_familytree(file_location):
    """
    Parses an initialization text file to build the starting family tree.
    Processes 'ADD_SPOUSE' commands directly and hands off others to process_input.
    """
    try:
        with open(file_location, "r", encoding="utf-8") as file:
            lines = file.readlines()
            
        for each_line in lines:
            # Skip empty lines
            if not each_line.strip():
                continue
            
            # Direct handling for spouse initialization lines
            if 'ADD_SPOUSE' in each_line:
                line = each_line.split()
                member = line[1].lower()
                
                if member in family:
                    member_obj = family[member]
                    spouse_name = line[2].lower()
                    spouse_gender = line[3].lower()
                    
                    # Create and cross-link both Person instances
                    spouse_obj = Person(spouse_name, spouse_gender)
                    family[spouse_name] = spouse_obj
                    member_obj.spouse = spouse_obj
                    spouse_obj.spouse = member_obj
            else:
                # Delegate all other actions (e.g., ADD_CHILD) to command processor
                process_input(each_line)
        print('family tree created')
        
    except FileNotFoundError:
        print("File not found. Starting with empty/default tree.")
    
    
def process_input(inputs):
    """
    Routes command strings to their corresponding tree operations.
    Validates parameter constraints before execution.
    """
    options = inputs.split()
    if not options:
        return
        
    command = options[0].upper()
    
    # Execution block for adding a new child
    if command == "ADD_CHILD":
        if len(options) == 4:
            mother_name = options[1].lower()
            child_name = options[2].lower()
            child_gender = options[3].lower()
    
            if mother_name in family:
                mother_obj = family[mother_name]
                mother_obj.ADD_CHILD(child_name, child_gender, family)
            else:
                print('PERSON_NOT_FOUND')
        else:
            print('Missing Arguments')
        
    # Execution block for searching relationships
    elif command == 'GET_RELATIONSHIP':
        if len(options) == 3:
            name = options[1].lower()
            relationship = options[2].lower()
            
            if name in family:
                name_obj = family[name]
                relationships = name_obj.GET_RELATIONSHIP(relationship)
                if relationships:
                    print(" ".join(relationships))
                else:
                    print("NONE")
            else:
                print('PERSON_NOT_FOUND')
        else:
            print('Missing Arguments')


# ==========================================
# RUNTIME ENTRY POINT
# ==========================================

# Initialize the base ancestors
family = {}
arthur = Person('king arthur', 'male')
margaret = Person('margaret', 'female')

# Registry setup
family['arthur'] = arthur
family['margaret'] = margaret

# Marriage linkage
arthur.spouse = margaret
margaret.spouse = arthur

# Initialize via text file batch commands
file_location = input('Enter the text File location to create family tree: ')
create_familytree(file_location)

# Continuous interactive loop
while True:    
    print("\nFamily Tree System\nOptions:\n1. ADD_CHILD [mother_name] [child_name] [child_gender]\n2. GET_RELATIONSHIP [name] [relationship_type]\n3. Exit")
    inputs = input("Enter your command: ")
    if inputs.strip().lower() == "exit":
        break
    else:
        process_input(inputs)


# In[ ]:





# In[ ]:





# In[ ]:




