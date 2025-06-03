import os
import string

dirname = os.path.dirname(__file__)

resource_file_path = os.path.join(dirname, './resource_1.txt')

result_file_path = os.path.join(dirname, './result_1.txt')

with open(resource_file_path, 'r') as resource_file:
  text = resource_file.read()

translator = str.maketrans('', '', string.punctuation)
words = text.translate(translator).split()

word_counts = {}
for word in words:
  if word in word_counts:
    word_counts[word] += 1
  else:
    word_counts[word] = 1

data_sorted = sorted(word_counts.items(), key=lambda x: (-x[1], x[0]))

with open(result_file_path, 'w') as result_file:
  for word, count in data_sorted:
    result_file.write(f'{word} {count}\n')
