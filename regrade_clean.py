import pandas as pd
import sys
import shelp
from canvasapi import Canvas
import glob
import tempfile
import os
# functions

# vars
assignment_name = input("Enter test name: ")

# main
shelp.make_dir_if_missing("output")

if len(sys.argv) != 3:
    print("Usage: python regrade.py <gradebooks/> <regrades.xlsx>")
    sys.exit(1)

"""
# validate regrade file
for fname in sys.argv[2:]:
    if shelp.get_file_type(fname) != ".csv":
        print(f"Usage: {fname} must be of type '.csv'")
        sys.exit(1)
shelp.remove_bom(sys.argv[2])
"""



# validate dirs
shelp.validate_dir(sys.argv[1])
shelp.validate_dir("additional_feedback")



gBooks = [pd.read_csv(os.path.join(sys.argv[1],gbookpath)) for gbookpath in os.listdir(sys.argv[1])]
# combine gradebooks to find Canvas ID
combined_gbook = pd.DataFrame()
for i, gbook in enumerate(gBooks):
    combined_gbook = pd.concat([combined_gbook, gbook])


#regrades = pd.read_csv(sys.argv[2], encoding='latin-1')
regrades = pd.read_excel(sys.argv[2], sheet_name=None)
regrades = list(regrades.values())[0]

# strip whitespace
regrades.loc[regrades["action required"].notna(), "action required"] = regrades["action required"].str.strip()

# make no change string uniform
regrades = regrades.replace("none", None, regex=False).reset_index(drop=True)
regrades = regrades.replace("no change", None, regex=False)
regrades = regrades.replace("No change", None, regex=False)
regrades = regrades.replace("No change.", None, regex=False)
regrades = regrades.replace("no change.", None, regex=False)

pd.set_option('display.max_rows', None)
print(regrades['action required'])

# extract grade changes as ints
regrades.loc[regrades["action required"].notna(), "action required"] = regrades["action required"].astype(str)
regrades.loc[regrades["action required"].notna(), "scoreChange"] = regrades["action required"].str.split().str[0].astype("Int64")
regrades.loc[regrades["action required"].isna(), "scoreChange"] = 0

regrades = pd.merge(regrades, combined_gbook[["ID", "SIS User ID", assignment_name]],
                    how='left',
                    left_on='student #',
                    right_on='SIS User ID')

# format comments
regrades.loc[regrades["comments"].isnull(), "comments"] = "*No comments left by regrader*"
regrades["feedback"] = "Question regraded: Q." + regrades["Question for review"].astype(str) + "\n\nChange in grade: " + regrades['scoreChange'].astype(str) + "\n\nComments left by regrader: " + regrades["comments"].astype(str)

# aggregate grade changes
regrades["scoreChangeSum"] = regrades.groupby(["ID", "SIS User ID"])["scoreChange"].transform("sum")

# format grades for upload to Canvas
regrades['initialScore'] = regrades[assignment_name]
regrades['newScore'] = regrades['initialScore'].astype("float").astype("Int64") + regrades['scoreChangeSum'].astype("float").astype("Int64")


# organise output
regrades_final = regrades[["ID", "SIS User ID", "initialScore", "scoreChangeSum", "newScore", "feedback"]]
regrades_final.to_csv('output/regrades.csv', index=False)

print("duplicates:")
print(regrades[regrades.duplicated(subset=['ID'], keep=False)])