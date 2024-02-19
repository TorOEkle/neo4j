CREATE TABLE Persons (
    personal_number INT PRIMARY KEY,
    first_name VARCHAR(255),
    family_name VARCHAR(255),
    age INT,
    sex VARCHAR(50),
    occupation VARCHAR(255),
    activity VARCHAR(255)
    partner_personal_number INT NULL,
    family_id INT,
    FOREIGN KEY (partner_personal_number) REFERENCES Persons(personal_number),
    FOREIGN KEY (family_id) REFERENCES Families(family_id)
);

CREATE TABLE Families (
    family_id INT  PRIMARY KEY,
    family_name VARCHAR(255) NULL
);


CREATE TABLE Households (
    household_id INT PRIMARY KEY,
    address VARCHAR(255),
);

CREATE TABLE HouseholdMembers (
    household_id INT,
    personal_number INT,
    PRIMARY KEY (household_id, personal_number),
    FOREIGN KEY (household_id) REFERENCES Households(household_id),
    FOREIGN KEY (personal_number) REFERENCES Persons(personal_number)
);

CREATE TABLE ParentChild (
    parent_personal_number INT,
    child_personal_number INT,
    PRIMARY KEY (parent_personal_number, child_personal_number),
    FOREIGN KEY (parent_personal_number) REFERENCES Persons(personal_number),
    FOREIGN KEY (child_personal_number) REFERENCES Persons(personal_number)
);