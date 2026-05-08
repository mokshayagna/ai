import json

student={
  "name": "Moksha",
  "age": 21,
  "isStudent": "yes",
  "skills": ["C", "Python", "Embedded Systems"],
  "address": {
    "city": "Bangalore",
    "pincode": 560001
  }
}

print(type(student))
data = json.load(student)
print(type(data))
