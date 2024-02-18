from simulations import set_family 
from utils import time_it, people,get_names ,get_random_data, assign_addresses_to_households

@time_it
def main():
    N = 10
    data = get_random_data(N)
    female_firstname,male_firstname = get_names(data)

    persons = people(data=data, N=N,female_names=female_firstname, male_names=male_firstname)

    families,households= set_family(persons)

    numberOfHousholds = len(households)
    assign_addresses_to_households(households, numberOfHousholds)

if __name__ == "__main__":

    main()
