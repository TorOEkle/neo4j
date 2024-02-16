

class Person:
    def __init__(self, age, sex, work, name=None):
        self.age = age
        self.sex = "Male" if sex ==1 else "Female"
        self.occupation = work
        self.marital_status = "single"
        self.family_name = None
        self.first_name = name
        self.partner = None
        self.children = []
        self.parents = []

    def set_partner(self, partner):
        self.partner = partner
        partner.partner = self

    def set_family_name(self, new_name):
        self.family_name = new_name

    def add_child(self, child):
        if child not in self.children:
            self.children.append(child)

        if self.partner and child not in self.partner.children:
            self.partner.children.append(child)

    def __str__(self):
        partner_info = (
            f"Partner: {self.partner.first_name} {self.partner.family_name}"
            if self.partner
            else "No Partner"
        )
        parent_names = ", ".join(
            [p.first_name + " "+ str(p.age) for p in self.parents]
        )
        children_names = ", ".join(
            [c.first_name + " "+ str(c.age) for c in self.children]
        )
        return (f"{self.first_name} {self.family_name} (Age: {self.age}, Sex: {self.sex}, {partner_info}, Parents: [{parent_names}], Children: [{children_names}])")
    