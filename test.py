
from canvasapi import Canvas
import glob
import tempfile
import os
import re

API_URL = "https://ubc.instructure.com"
with open("token.txt","r") as f:
    API_KEY = f.read()
canvas = Canvas(API_URL, API_KEY)

feedbackdir = "additional_feedback"

canvas_course_id = input('Canvas course ID: ')
canvas_course_id = int(canvas_course_id)
canvas_assignment_id = input('Canvas assignment ID: ')
canvas_assignment_id = int(canvas_assignment_id)
canvas_id = int(input('Student Canvas ID: '))

course = canvas.get_course(canvas_course_id)
assignment = course.get_assignment(canvas_assignment_id)

feedback = input('input feedback: ')
grade = input('student grade: ')

try:
    submission = assignment.get_submission(canvas_id)
except:
    print('Could not find assignment for {}'.format(canvas_id))

try:
    score = float(grade)
    print("Uploading grade for {} ...".format(canvas_id))
    submission.edit(submission={'posted_grade': score},
                    comment={'text_comment': feedback})
except:
    print(f"No change in grade for {canvas_id} ...")