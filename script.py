# Python program to execute
# main directly

print ("Always executed")

if __name__ == "__main__":
	print ("Executed when invoked directly")
else:
	print ("Executed when imported")
# Python program to use
# main for function call.

import myscript
myscript.my_function()


for i in range(1, 10):
	print(i)