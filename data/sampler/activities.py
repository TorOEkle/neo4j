import numpy as np
import pandas as pd
from pathlib import Path
import random



def extracurricular_activity(ages):

    activity = np.zeros(len(ages))  # Initialize all as 0
    print(activity)

    # List of possible extracurricular activities
    activities = ["Football", "American football", "Volleyball", "Tennis", "Basketball", "Chess"]

    # Dictionary to store assigned activities
    assigned_activities = {}

    # Assign a random activity to each student
    for person in range(len(ages)):
        if 6 <= ages[person] <=18: # Set limit for age range (can change this.)
            assigned_activities[person] = random.choice(activities)
        else:
            assigned_activities[person] = None


    # print(len(np.array(list(assigned_activities.values()))))
    assigned_activities = np.array(list(assigned_activities.values())) # Create a array from the dict. 
    return assigned_activities