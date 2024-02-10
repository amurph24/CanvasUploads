import pandas as pd
import sys
import shelp
from canvasapi import Canvas
import glob
import tempfile
import os
# functions

# vars

# main
shelp.make_dir_if_missing("output")

if len(sys.argv) != 3:
    print("Usage: python regrade.py <gradebooks/> <regrades.csv>")
    sys.exit(1)

# validate regrade file
for fname in sys.argv[2:]:
    if shelp.get_file_type(fname) != ".csv":
        print(f"Usage: {fname} must be of type '.csv'")
        sys.exit(1)
shelp.remove_bom(sys.argv[2])

# validate dirs
shelp.validate_dir(sys.argv[1])
shelp.validate_dir("additional_feedback")



gBooks = [pd.read_csv(os.path.join(sys.argv[1],gbookpath)) for gbookpath in os.listdir(sys.argv[1])]
regrades = pd.read_csv(sys.argv[2], encoding='latin-1')

# make no change string uniform
regrades = regrades.replace("none", None, regex=False).reset_index(drop=True)
regrades = regrades.replace("no change", None, regex=False)
regrades = regrades.replace("No change", None, regex=False)

# remove requests with no grade change
#regrades = regrades.drop(regrades[regrades["action required"].isna()].index).reset_index(drop=True)

# convert action required to usable ints
#regrades.loc[regrades["action required"] != None, "initialScore"] = regrades["action required"].str.split().str[0].astype("Int64")
#regrades.loc[regrades["action required"] != None, "scoreChange"] = regrades["action required"].str.split().str[2].astype("Int64") - regrades["initialScore"]

regrades.loc[regrades["action required"] != None, "scoreChange"] = regrades["action required"].str.split().str[0].astype("Int64")

# combine gradebooks to find Canvas ID
combined_gbook = pd.DataFrame()
for i, gbook in enumerate(gBooks):
    combined_gbook = pd.concat([combined_gbook, gbook])

#test_name = input("Test name: ")

regrades = pd.merge(regrades, combined_gbook[["ID", "SIS User ID", "Test 2"]],
                    how='left',
                    left_on='studentNum',
                    right_on='SIS User ID')

# aggregate grade changes
regrades["scoreChangeSum"] = regrades.groupby(["ID", "SIS User ID"])["scoreChange"].transform("sum")
# format comments
regrades.loc[regrades["comments"].isnull(), "comments"] = "No comments left by marker"
print(regrades["comments"])
regrades["feedback"] = regrades["Q for review"].astype(str) + regrades["comments"].astype(str)
print(regrades["feedback"])

regrades = regrades.drop_duplicates(subset=["ID", "SIS User ID"], keep="last")
regrades = regrades.reset_index(drop=True)

# format grades for upload to Canvas
regrades['initialScore'] = regrades['Test 2']
regrades['newScore'] = regrades['initialScore'].astype("float").astype("Int64") + regrades['scoreChangeSum'].astype("float").astype("Int64")


# organise output
regrades_final = regrades[["ID", "SIS User ID", "initialScore", "scoreChangeSum", "newScore", "comments"]]
regrades_final.to_csv('output/regrades.csv', index=False)

print("duplicates:")
print(regrades[regrades.duplicated(subset=['ID'], keep=False)])