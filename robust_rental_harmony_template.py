#This template is meant to be used with iPython,
#ideally in the Spyder IDE where you can run blocks of code 
#delineated by "#%%" with a single kebyoard shortcut.

#%%
#Modify this line to match the folder where you unzipped "rental_harmony.zip":
location_of_this_script = "/Users/shri/Downloads/rentdivision-master"
import sys
sys.path.append(location_of_this_script)

#%%
from robust_rental_harmony import rental_harmony
import pandas as pd

#%%
#Enter the total rent here:
total_rent = 13500
total_rent

#%%
#Have each housemate choose their least-favorite room, and assign it
#a marginal value of zero dollars.  Then, ask them to imagine living in 
#that room and paying slightly-less-than-average rent.  How much extra 
#would they be willing to pay to move into each other room?  
#Enter those values here:
values = pd.DataFrame({
#    Room       :    0      1      2      3      4      5      6      7      8      9
    'Alice'     :   [1600,    200,    300,    400,    200,    150,    200,    200,    100,   0  ],
    'Bob'       :   [1100,   32,    23,    0,    180,   150,   120,   90,    60,   30 ],
    'Caitlin'   :   [1200,    204,   29,    0,    175,   140,   100,   70,    40,   15 ],
    'Dave'      :   [1200,    26,    212,   0,    190,   160,   130,   95,    55,   20 ],
    'Emma'      :   [1000,   150,   120,   90,   60,    30,    0,    210,   170,   140],
    'Frank'     :   [1100,   130,   100,   70,   40,    10,    190,   0,    220,   180],
    'Grace'     :   [1000,   110,   80,    50,   20,    0,    170,   140,   110,   200],
    'Henry'     :   [1050,   90,    60,    30,   0,    180,   150,   120,   90,    60 ],
    'Ivy'       :   [900,   70,    40,    10,   190,   0,    220,   180,   150,   120],
    'Jack'      :   [1000,    50,    20,    0,   170,   140,   110,   80,    230,   190]
    }).T

values.columns = ['Room 0', 'Room 1', 'Room 2', 'Room 3', 'Room 4', 'Room 5', 'Room 6', 'Room 7', 'Room 8', 'Room 9']
#values.columns
#%%
#Compute the (room,price) assignment that is maximally-far from 
#creating ency between any two housemates; this assignment
#necessarily also maximizes the total utility of the group,
#measured in marginal dollars:
(solution,envies,envy_free) = rental_harmony(total_rent,values)
solution

#%%
envies
#%%
envy_free
# %%
url = 'https://docs.google.com/spreadsheets/d/1RMYYparf7i1n2-oUQUxL4g6fv8uv-wSZCyLYidB75Ak/export?format=csv'
pd.read_csv(url)
# %%
