def correct_scores(incorrect_scores):
    correct_scores = [53, 64, 75, 19, 92]
    corrected_scores = [correct_scores[incorrect_scores.index(score)] for score in incorrect_scores]
    return corrected_scores

incorrect_scores = [35, 46, 57, 91, 29]
corrected_scores = correct_scores(incorrect_scores)
print(corrected_scores)

from collections import Counter

text = "Hello welcome to Cathay 60th year anniversary"
filtered_text = [char.upper() for char in text if char.isalnum()]
counter = Counter(filtered_text)

for char in sorted(counter):
    print(f"{char} {counter[char]}")

def josephus(n):
    people = list(range(1, n + 1))
    index = 0
    while len(people) > 1:
        index = (index + 2) % len(people)
        people.pop(index)
    return people[0]

n = int(input("Please enter the number of people n (0-100): "))

if 0 < n <= 100:
    print(f"The last person remaining is in position {josephus(n)}.")
else:
    print("Please enter a valid value for n (1-100).")

