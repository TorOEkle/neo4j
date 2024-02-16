class Household:
    def __init__(self, Family):
        self.members = []
        self.address = None
        self.children_limit = 3
        self.extended_family = Family

    def add_member(self, person):
        if person.age < 18:
            if not self.can_add_child():
                return False

        if not any(m.age >= 18 for m in self.members):
            self.family_name = person.family_name
        self.members.append(person)
        return True

    def can_add_child(self):
        return (
            len([member for member in self.members if member.age < 18])
            < self.children_limit
        )

    def set_address(self, address):
        self.address = address

    def __str__(self):
        address_description = (
            f"Address: {self.address}" if self.address else "No Address"
        )
        household_members = "\n  ".join([str(member) for member in self.members])
        return f"Household of the Family living in \n  {address_description}\n  Members:\n{household_members}\n"