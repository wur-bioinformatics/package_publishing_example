IUPAC_REVERSE_COMPLEMENT = { # Thanks, ChatGPT!
    'A': 'T',  'a': 't',  # Adenine
    'T': 'A',  't': 'a',  # Thymine
    'C': 'G',  'c': 'g',  # Cytosine
    'G': 'C',  'g': 'c',  # Guanine
    'R': 'Y',  'r': 'y',  # Purines: A or G → T or C
    'Y': 'R',  'y': 'r',  # Pyrimidines: C or T → A or G
    'S': 'S',  's': 's',  # Strong: G or C → G or C
    'W': 'W',  'w': 'w',  # Weak: A or T → A or T
    'K': 'M',  'k': 'm',  # Keto: G or T → A or G
    'M': 'K',  'm': 'k',  # Amino: A or C → T or C
    'B': 'V',  'b': 'v',  # Not A: C, G, or T → A, C, or G
    'D': 'H',  'd': 'h',  # Not C: A, G, or T → A, T, or C
    'H': 'D',  'h': 'd',  # Not G: A, C, or T → A, C, or G
    'V': 'B',  'v': 'b',  # Not T: A, C, or G → C, G, or T
    'N': 'N',  'n': 'n',  # Any base → any base
}

class InvalidIUPACError(Exception):
  pass

def comp(letter: str) -> str:
  """
  Somewhat 'safe' version of using the IUPAC lookup table.

  Examples:
    >>> comp('A')
    'T'

    >>> comp('N')
    'N'
  
  Args:
    letter (str): 1 letter nucleotide string which will be complemented with the IUPAC lookup table

  Returns:
    str: complemented nucleotide allowing for IUPAC degeneracies
  """
  assert len(letter) == 1, f'Length of input must be 1, got {len(letter)}'
  try:
    return IUPAC_REVERSE_COMPLEMENT[letter]
  except ValueError:
    raise InvalidIUPACError(f'{letter} is not a valid IUPAC code')

def revcomp(input: str) -> str:
  complement = [comp(letter) for letter in input]
  return ''.join(complement[::-1])
