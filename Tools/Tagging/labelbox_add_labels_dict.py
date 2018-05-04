'''
This is the code used in LabelBox to label the Paul images. 
'''

[
  {
    "name": "Age",
    "instructions": "How old is Paul?",
    "type": "radio",
    "required": true,
    "options": [
      {
        "value": "young_adult",
        "label": "Young adult"
      },
      {
        "value": "middle_age",
        "label": "Middle age"
      },
      {
        "value": "older",
        "label": "Older"
      }
    ]
  },
  {
    "name": "Facial_Hair",
    "instructions": "Does Paul have facial hair?",
    "type": "radio",
    "required": false,
    "options": [
      {
        "value": "moustache",
        "label": "Moustache"
      },
      {
        "value": "beard",
        "label": "Beard"
      },
    ]
  },
  {
    "name": "Anlge",
    "instructions": "What is the angle of Paul’s face?",
    "type": "radio",
    "required": true,
    "options": [
      {
        "value": "font_angle",
        "label": "Front"
      },
      {
        "value": "side_angle",
        "label": "Side"
      },
    ]
  },
]