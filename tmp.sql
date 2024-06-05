CREATE TABLE Persons (
    person_id INT PRIMARY KEY,
    first_name VARCHAR(255),
    family_name VARCHAR(255),
    age INT,
    sex VARCHAR(50),
    occupation VARCHAR(255),
    marital_status VARCHAR(100),
    partner_id INT,
    family_id INT,
    FOREIGN KEY (partner_id) REFERENCES Persons(person_id),
    FOREIGN KEY (family_id) REFERENCES Families(family_id)
);

CREATE TABLE Families (
    family_id INT PRIMARY KEY,
    family_name VARCHAR(255)
);

CREATE TABLE Households (
    household_id INT PRIMARY KEY,
    address VARCHAR(255),
    children_limit INT
);

CREATE TABLE HouseholdMembers (
    household_id INT,
    person_id INT,
    PRIMARY KEY (household_id, person_id),
    FOREIGN KEY (household_id) REFERENCES Households(household_id),
    FOREIGN KEY (person_id) REFERENCES Persons(person_id)
);
