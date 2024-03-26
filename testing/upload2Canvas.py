#author: Patrick Walls, adapted by Aidan Murphy

from canvasapi import Canvas
import pandas as pd
import glob
import tempfile
import os
import re
import sys

API_URL = "https://ubc.instructure.com"
with open("token.txt","r") as f:
    API_KEY = f.read()
canvas = Canvas(API_URL, API_KEY)

feedbackdir = "additional_feedback"

canvas_course_id = input('Canvas course ID: ')
canvas_course_id = int(canvas_course_id)
canvas_assignment_id = input('Canvas assignment ID: ')
canvas_assignment_id = int(canvas_assignment_id)

course = canvas.get_course(canvas_course_id)
assignment = course.get_assignment(canvas_assignment_id)

# read regrade.csv
regrades = pd.read_csv('output/regrades.csv')
# assign failed uploads df
failed = pd.DataFrame()

for index, row in regrades.iterrows():
    canvas_id = int(float(row['ID']))
    student_num = int(float(row['SIS User ID']))
    print("------------------------------------------------------\n")
    print(f"Canvas ID: {canvas_id}\tStudent Number: {student_num}")

    try:
        submission = assignment.get_submission(canvas_id)
    except:
        print('Could not find assignment for {}'.format(canvas_id))
        continue

    try:
        score = int(float(row['newScore']))
        feedback = row['feedback']
        print("Uploading grade & comments for {} ...".format(canvas_id))
        submission.edit(submission={'posted_grade': score},
                        comment={'text_comment': feedback})
    except:
        print(f"something went wrong for student: {row['SIS User ID']}, grades and/or feedback could not be uploaded")
        # TODO Test failed upload:
        failed.concat(row)


sys.exit(0)


"""  
# find feedback file if it exists
regex = re.compile(f'.*{student_num}\.pdf$')
source = ""
for root, dirs, files in os.walk(feedbackdir):
    for file in files:
        if regex.match(file):
            print(f"feedback file matching student num:{student_num} found, using file: {file}")
            source = os.path.join(feedbackdir, file)

# error handling if no feedback file
if len(source) == 0:
    print(f'Could not find feedback .pdf file for {canvas_id}')
    continue
else:
    print("Uploading feedback for {} ...".format(canvas_id))
    submission.upload_comment(source)
"""

"""
f = tempfile.NamedTemporaryFile('w+')
f.name = '{}_autograded.ipynb'.format(assignment_name)
with open(source,'r') as fsource:
    f.write(fsource.read())
f.seek(0)
submission.upload_comment(f)
f.close()
"""