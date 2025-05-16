from collections import Counter

resource_file_path = './resource_1.txt'

result_file_path = 'result_1.txt'

with open(resource_file_path, 'r') as resource_file:
  words = resource_file.read().split()

data = Counter(words).most_common()

data_sorted = sorted(data, key=lambda x: (-x[1], x[0]))

with open(result_file_path, 'w') as result_file:
  for word, count in data_sorted:
    result_file.write(f'{word} {count}\n')
