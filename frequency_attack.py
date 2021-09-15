# Dmitriy Kagno 9/15/21

# Extract the frequency list for the english language
# I got this data from this webpage: http://pi.math.cornell.edu/~mec/2003-2004/cryptography/subs/frequencies.html
def get_eng_freq_list(file):
  freq_file = open(file, "r")
  char_list = {}

  for line in freq_file:
    # The data is formatted awkwardly so I extracted the first column (english letter)
    # and the last column (frequency as a percentage)
    key = line.split()[0]
    value = line.split()[3]
    char_list[key] = float(value)
  
  sorted_char_list = dict(sorted(char_list.items(), reverse=True, key=lambda item: item[1]))
  freq_file.close()
  return sorted_char_list


# Create a character frequency list from all of the characters inside of some input text
def get_input_freq_list(file):
  input_file = open(file, 'r')
  char_list = {}

  # Go through every char in the input text and add it to a list if it isn't there already
  # This loop also keeps track of the number of times the char appears in the input text
  for line in input_file:
    for char in line:
      if char == '\n' or char == ' ':
        continue
      elif char not in char_list.keys():
        char_list[char] = 0
      else:
        char_list[char] += 1 
  
  # Convert the number of character appearances into a percentage
  total_chars = sum(char_list.values())
  for char, appearances in char_list.items():
    char_list[char] = round(appearances / total_chars * 100, 2)

  sorted_char_list = dict(sorted(char_list.items(), reverse=True, key=lambda item: item[1]))
  input_file.close()
  return sorted_char_list


# Helper method to extract user made character equivalence list
def import_char_equiv_list(file):
  char_equiv_file = open(file, "r")
  char_equiv_list = {}

  for line in char_equiv_file:
    # Take the first char of the each column
    cypher_char = line.split(',')[0][0]
    plaintxt_char = line.split(',')[1][0] 
    char_equiv_list[cypher_char] = plaintxt_char

  char_equiv_file.close()
  return char_equiv_list


# Primative frequency attack that blindly swaps characters in the input text based on frequency
def bad_freq_attack(file, mapping):
  input_file = open(file, 'r')
  output_file = open("./bad_freq_attack.txt", "w")

  for line in input_file:
    for char in line:
      if char == "\n" or char == ' ' or char == '.':
        output_file.write(char)
      else:
        output_file.write(mapping[char])
  
  input_file.close()
  output_file.close()


# Better frequency attack that checks user made character equivalence list before swapping based on frequency
def better_freq_attack(file, mapping, imported_mapping):
  input_file = open(file, 'r')
  output_file = open("./better_freq_attack.txt", "w")

  for line in input_file:
    for char in line:
      if char == "\n" or char == ' ' or char == '.':
        output_file.write(char)
      elif char in imported_mapping.keys():
        output_file.write(imported_mapping[char])
      else:
        output_file.write(mapping[char])
  
  input_file.close()
  output_file.close()


# Main method to run frequency attack
def decipher():
  input_file = "./input.txt"
  eng_freq_list_file = "./eng_freq_list.txt"
  equiv_list_file = './character_equiv_list.txt'

  input_freq_list = get_input_freq_list(input_file)
  eng_freq_list = get_eng_freq_list(eng_freq_list_file)
  imported_char_equiv_list = import_char_equiv_list(equiv_list_file)

  # Stitch together input frequency list and english frequency list such that
  # their characters are aligned based on their frequency percentage
  char_equiv_list = dict(map(lambda key, value: key + value, input_freq_list.keys(), eng_freq_list.keys()))
  
  bad_freq_attack(input_file, char_equiv_list)
  better_freq_attack(input_file, char_equiv_list, imported_char_equiv_list)
  pass


decipher()