from . import sampler
import pandas as pd
# from collections import Counter

N = 50

# households = pd.DataFrame(sampler.sample_household(N))
# type_count = households["type"].value_counts().to_dict()
# type_count = Counter(households["type"])  # Alternative
# addresses = sampler.sample_address(type_count)

# apartments = sampler.sample_apartment(type_count)

# cadaster = sampler.make_cadaster()
# print(sampler.sample_group(cadaster, type_count))
# print(cadaster.group_sample(type_count))

address1 = "Nedre Tordenskjolds gate 11A, Stavanger, Norway"
address2 = "Skarahødden 23, Sandnes, Norway"

distance_km = sampler.address_distance(address1, address2)
print(f"The distance between the addresses is approximately {distance_km:.2f} kilometers.")
