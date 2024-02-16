from simulations import set_family 
from housing_families import assign_addresses_to_households
from utils import time_it, people,get_names ,get_random_data


@time_it
def main():
    N = 10000
    data = get_random_data(N)
    female_firstname,male_firstname = get_names(data)

    persons = people(data=data, N=N,female_names=female_firstname, male_names=male_firstname)
    families,households= set_family(persons)

    numberOfHousholds = len(households)
    assign_addresses_to_households(households, numberOfHousholds)

    print("Households Overview:")
    for household in households:
        print(household)
    print("\n")


    print("People withiout names")
    for p in persons:
        if p.family_name == None:
            print(p)


    print("Households without adresses")
    for household in households:
        if household.address == None:
            print(household)

    
if __name__ == "__main__":

    main()
