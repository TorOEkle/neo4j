import numpy as np
import pandas as pd
import zipfile
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from pathlib import Path


# setting seed
np.random.seed(42)


## Helper functions
def normalize(array):
    return array / np.sum(array)


def between(array, lower, upper):
    return (lower <= array) & (array <= upper)


def group_size(array):
    return np.count_nonzero(array)


def read_csv_zip(path, **kwargs):
    def split(path):
        """
        Splits "/path/directory.zip/file.csv" into ("/path/directory.zip", "file.csv")
        """
        directory = path
        while directory.suffix != ".zip" and directory != directory.parent:
            directory = directory.parent
        return directory, path.relative_to(directory)

    zip_directory, filepath = split(Path(path))

    with zipfile.ZipFile(zip_directory) as z:
        # Note: filenames in Windows are case-insensitive
        # but filenames in ZIP directories are case-sensitive
        with z.open(str(filepath)) as f:
            return pd.read_csv(f, **kwargs)

    
## Group assigners
def assign_constant_group(array, group, constant):
    array[group] = constant


def assign_bernoulli_group(array, group, p):
    array[group] = bernoulli_trial(p=p, size=group_size(group))


## Data wrappers
def _house_address():
    address = read_csv_zip(
        './matrikkel.zip/matrikkelenAdresse.csv',
        sep=';',
        header=0,
        dtype={
            "adressetilleggsnavn": str,
            "adressetilleggsnavnKilde": str,
        },
    )
    
    # Filter adresser based on values in column 'kommunenummer'
    address = address[address['kommunenavn'].isin(['SANDNES', 'STAVANGER'])]

    # Remove rows where adressenavn = NAN
    address = address.dropna(subset=['adressenavn'])
    # address = address.reset_index()
    # address = address[['lokalid', 'kommunenavn', 'adressetype',
    #        'adressenavn', 'nummer', 'adresseTekst', 'Nord', 'Øst',
    #        'postnummer', 'poststed', 'grunnkretsnavn',
    #        'soknenummer', 'soknenavn']]
    address['nummer'] = address['nummer'].astype(int)

    return address


def _apartment_address():
    region1 = read_csv_zip(
        "./matrikkel.zip/matrikkelenAdresseLeilighetsnivaSandnes.csv",
        sep=";",
        dtype={
            "uuidAtkomst": str,
        },
    )
    region2 = read_csv_zip(
        "./matrikkel.zip/matrikkelenAdresseLeilighetsnivaStavanger.csv",
        sep=";",
        dtype={
            "adressetilleggsnavn": str,
            "adressetilleggsnavnKilde": str,
        },    
    )
    
    # Concatenate the two dataframes
    address = pd.concat([region1, region2])

    # # Change adressekode to integer
    # apartments.loc[:, 'adressekode'] = apartments['adressekode'].astype(int)

    # Change nummer to string
    address['nummer'] = address['nummer'].astype(str)

    # Create a new column with "kommunenavn", adresseTekst". This is to correct for same adresses in both Stavanger and Sandnes
    address['kommune_adresse'] = address['kommunenavn'] + ', ' + address['adressenavn'] + ' ' + address['nummer']

    ## I want to filter out all the adresses that have count above 1
    address_count = address.groupby('kommune_adresse')['kommune_adresse'].transform('count')

    ## Filter on at least 4 apartments in the same address
    address = address[address_count > 4]
    
    return address


def make_cadaster():
    address = _house_address()
        
    ## Looks for rows where adressenavn ends with a number and a letter.
    # This is then terrace houses
    house_address =         address[~pd.isna(address['bokstav'])]
    terrace_house_address = address[ pd.isna(address['bokstav'])]
    apartment_address = _apartment_address()

    return {
        "house": house_address,
        "terrace-house": terrace_house_address,
        "apartment": apartment_address,
    }

## Distance
def latlon(location):
    return location.latitude, location.longitude


def address_distance(address1, address2):
    geolocator = Nominatim(user_agent="address_distance_calculator")

    # Get the latitude and longitude coordinates for the two addresses
    location1 = geolocator.geocode(address1)
    location2 = geolocator.geocode(address2)

    if location1 is None or location2 is None:
        return float("nan")

    # Calculate the distance using geodesic function
    distance = geodesic(latlon(location1), latlon(location2)).kilometers

    return distance


## Random samplers
def bernoulli_trial(p, size):
    return np.random.binomial(n=1, p=p, size=size)


def sample_feature(f):
    if isinstance(f, (str, int, float)):
        return f
    elif isinstance(f, range):
        return np.random.randint(f.start, f.stop)
    else:
        raise TypeError


def sample_age(size):
    # Define the age intervals and corresponding probabilities for each year
    age_intervals = np.arange(0, 83)
    age_probs = np.array([
        0.006, 0.008, 0.01, 0.012, 0.015, 0.018, 0.022, 0.025, 0.028, 0.03,
        0.032, 0.034, 0.036, 0.038, 0.04, 0.041, 0.042, 0.043, 0.044, 0.044,
        0.043, 0.042, 0.041, 0.04, 0.039, 0.037, 0.036, 0.035, 0.034, 0.033,
        0.032, 0.031, 0.031, 0.031, 0.031, 0.032, 0.033, 0.034, 0.035, 0.036,
        0.038, 0.04, 0.042, 0.044, 0.046, 0.048, 0.05, 0.052, 0.054, 0.056,
        0.057, 0.058, 0.058, 0.058, 0.058, 0.057, 0.056, 0.055, 0.054, 0.053,
        0.052, 0.051, 0.05, 0.049, 0.048, 0.047, 0.046, 0.045, 0.044, 0.043,
        0.042, 0.041, 0.04, 0.039, 0.038, 0.037, 0.036, 0.035, 0.034, 0.033,
        0.032, 0.031, 0.03
    ])

    # Normalize age_probs to sum to 1
    age_probs = np.array(age_probs) / np.sum(age_probs)

    # Generate the Age column
    return np.random.choice(age_intervals, size=size, p=age_probs)


def sample_sex(size):
    # Generate the Sex column
    return bernoulli_trial(p=0.5, size=size)


def sample_work(ages):
    # Generate the Work column based on age
    work = np.zeros(len(ages), dtype=np.bool_)  # Initialize all as 0

    # Update work status based on age conditions
    assign_constant_group(work, group=between(ages, 0, 17), constant=True)
    assign_bernoulli_group(work, group=between(ages, 18, 24), p=0.40)
    assign_bernoulli_group(work, group=between(ages, 25, 85), p=0.97)

    return work


def sample_student(ages):
    student = np.zeros(len(ages), dtype=np.bool_)  # Initialize all as 0

    assign_constant_group(student, group=between(ages, 0, 18), constant=True)
    # if you are between 18 and 24, you are a student with 60% probability
    assign_bernoulli_group(student, group=between(ages, 19, 24), p=0.60)

    return student


def sample_household(size):
    # Define the types of households
    houses = [
        {
            "type": "house",
            "share": 0.5,
            "rooms": range(3, 7),            # Number of rooms (between 3 and 7)
            "bathrooms": range(2, 4),        # Number of bathrooms (between 2 and 4)
            "size": range(100, 200),         # Size of the house (between 100 and 200 square meters)
            "lot_size": range(200, 500),     # Lot size (between 200 and 500 square meters)
            "build_year": range(1970, 2019),
            "people": range(1, 7),          # Number of people living in the household (between 1 and the number of rooms)
        },
        {
            "type": "apartment",
            "share": 0.3,
            "rooms": range(2, 5),            # Number of rooms (between 2 and 5)
            "bathrooms": range(1, 3),        # Number of bathrooms (between 1 and 3)
            "size": range(75, 150),          # Size of the house (between 75 and 150 square meters)
            "lot_size": range(100, 300),     # Lot size (between 100 and 300 square meters)
            "build_year": range(1980, 2019),
            "people": range(1, 5),          # Number of people living in the household (between 1 and the number of rooms)
        },
        {
            "type": "terrace-house",
            "share": 0.2,
            "rooms": range(1, 4),            # Number of rooms (between 1 and 4)
            "bathrooms": range(1, 2),        # Number of bathrooms (between 1 and 2)
            "size": range(50, 100),          # Size of the apartment (between 50 and 100 square meters)
            "lot_size": 0,                   # Lot size (0 for apartments)
            "build_year": range(1990, 2019),
            "people": range(1, 4),          # Number of people living in the household (between 1 and the number of rooms)
        },
    ]

    def get_feature(data, feature_name):
        return [value[feature_name] for value in data]

    def sample_features(table, index, f):
        # (slow since it's not vectorized)
        return np.array([sample_feature(table[i][f]) for i in index])

    def columns(table):
        return list(table[0].keys())

    # Generate data for 10 000 households
    sampled_houses = np.random.choice(a=len(houses), size=size, p=get_feature(houses, "share"))

    # Define a list to hold the data for each household
    return {
        feature: sample_features(houses, sampled_houses, feature)
        for feature in columns(houses)
    }


def shuffle_households(df):
    df = df[(1 <= df["people"]) & (df["people"] <= 4)]
    df = df.sample(frac=1)
    df = df.sort_values(by="people")
    return df


def sample_energy_label(build_year):
    # Define the energy labels
    energy_data = {
        "labels": ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
        "probs_by_decade": {
            "1970s": [0.01, 0.04, 0.15, 0.30, 0.25, 0.15, 0.10],
            "1980s": [0.02, 0.08, 0.20, 0.30, 0.20, 0.10, 0.10],
            "1990s": [0.10, 0.20, 0.25, 0.25, 0.10, 0.05, 0.05],
            "2000s": [0.20, 0.30, 0.25, 0.15, 0.05, 0.03, 0.02],
            "2010s": [0.40, 0.30, 0.15, 0.10, 0.03, 0.01, 0.01],
        },
    }

    decades = {
        "1970s": range(1970, 1979),
        "1980s": range(1980, 1989),
        "1990s": range(1990, 1999),
        "2000s": range(2000, 2009),
        "2010s": range(2010, 2019),
    }

    # Add the energy label to each household
    energy_label = np.empty_like(build_year, dtype=np.str_)
    for decade_name, decade in decades.items():
        decade_houses = between(build_year, decade.start, decade.stop)

        energy_label[decade_houses] = np.random.choice(
            energy_data["labels"],
            size=group_size(decade_houses),
            p=energy_data["probs_by_decade"][decade_name],
        )

    return energy_label


def sample_group(groups, group_size):
    return {
        group: groups[group].sample(size)
        for group, size in group_size.items()
    }


if __name__ == "__main__":
    # Create a dictionary to store the simulated data

    N = 2000
    ages = sample_age(N)
    data = {
        "age": ages,
        "sex": sample_sex(N),
        "work": sample_work(ages),
        "student": sample_student(ages),
    }

    print(data)

    # Convert the dictionary to a pandas DataFrame (optional, but convenient for data manipulation)
    df = pd.DataFrame(data)
    # Generate a student column based on age. = 1 for everyone under 18

    # Print the first few rows of the simulated dataset
    print(df.head())
