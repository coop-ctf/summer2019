"""
This is a puzzle.  Please call this program with exactly one command-
	line argument so that is computes successive approximations to pi.
If you give the correct input, this program will print out a sequence 
	converging to pi.  Since this sequence is by necessity infinite, 
	please terminate the program (<Ctrl-c>) when you are satisfied with
	your output.
Your answer must be the shortest possible input that, when provided
	as a command line argument to this program, will cause it to print
	a sequence converging to pi.
"""

import sys
import itertools as it

# Encode your input
def intify(char):
	char = ord(char)
	if char < 45:
		return char + 19
	if char < 48:
		return char + 16
	if char < 62:
		return char + 4
	if char < 92:
		return char - 65
	return char - 71

# Here's a hint
class Lock:
	x = y = None
	def __init__(self, x, y):
		self.x = x
		self.y = y
	def unlock(self, key):
		i = 0
		first_time = True
		for x, y in zip(it.cycle(range(self.x)),
						it.cycle(range(self.y))):
			if first_time:
				first_time = False
				i += 1
				continue
			if x == y == 0:
				if i == key:
					break
				i = 0
			i += 1

# Helper function; get the elements in an iterator until a repeat 
# is encountered.
def elts_before_repeats(iterator):
	s = set()
	for x in iterator:
		if x in s:
			return s
		s.add(x)

########################################################################
# PUZZLE TIME
########################################################################

if __name__ == "__main__":
	# This isn't part of the puzzle, give one command-line
	# argument please. 
	if len(sys.argv) != 2:
		raise ValueError("Invalid Input")
	inp = sys.argv[1]
	print("Your input:", inp)
	
	# Here begins the puzzle.  Can you encode the right input
	# properly?
	inp = [intify(x) for x in inp]

	print("Your input, decoded:", inp)
	if input("Continue? ([y]/n) ").lower().strip().startswith("n"):
		sys.exit(0)
	
	# Here's some hints for how the rest of the puzzle works.
	# (If you guess wrong, you will not be able to proceed.)
	Lock(3, 4).unlock(int(inp[0]))
	Lock(10, 6).unlock(int(inp[3]))

	# Now that you get how this works, can you get the right values
	# to use in the formula?
	c = i = a = b = 0
	while len(inp) > 5:
		c += inp[5] - inp[3]
		i += len(elts_before_repeats(zip(it.cycle(range(5)), 
							 			 it.cycle(range(3))))) / -inp[4]
		a += len(elts_before_repeats(zip(it.cycle(range(7)), 
							 			 it.cycle(range(4))))) - inp[1]
		b += inp[2] - len(elts_before_repeats(zip(it.cycle(range(7)), 
									  			 it.cycle(range(5)))))
		inp = inp[1:]

	print("c: %2i, i: %2i, a: %2i, b: %2i" % (c, i, a, b))
	if input("Continue? ([y]/n) ").lower().strip().startswith("n"):
		sys.exit(0)

	# Your output
	for x in it.accumulate(map(lambda x:c*(i)**x/(a*x+b),
							   it.count(0))):
		print(x)

########################################################################
# HELP
########################################################################

# If you're not familiar with the itertools library (it's great!), 
# here's a brief description of the functions used here.
# From: https://docs.python.org/3/library/itertools.html

## itertools.cycle(iterable)
## Make an iterator returning elements from the iterable and saving a 
## 	copy of each. When the iterable is exhausted, return elements from
## 	the saved copy. Repeats indefinitely.
## E.g. cycle('ABCD') --> A B C D A B C D ...

## itertools.accumulate(iterable[, func])
## Make an iterator that returns accumulated sums, or accumulated 
## 	results of other binary functions (specified via the optional func 
## 	argument).
## E.g. accumulate([1,2,3,4,5]) --> 1 3 6 10 15

## itertools.count(start=0, step=1)
## Make an iterator that returns evenly spaced values starting with 
## 	number start.
## E.g. count(10) --> 10 11 12 13 14 ...

########################################################################

# If you're not familiar, one way to approximate pi is to find an 
# infinite series converging to some simple function of pi.  Then, by 
# computing partial sums with more and more terms, we can get at better
# and better approximations of pi.  The more accuracy you want, the more
# terms you need to include in your sum.  This program, if given the 
# correct input, will print out the sequence of partial sums.  Please
# terminate the program (<Ctrl-c>) when you are satisfied.

########################################################################

# Have fun!