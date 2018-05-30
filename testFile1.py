def makesum(a,b):
	return a+product(b,a)

def product(a,b):
	return exponent(a,b);

def exponent(a,b):
	return a**b 

def main():
	a=2
	b=3
	res=makesum(a,b)

	print("Final Computed Result",res)

main()



