from _fib import lib

def print_fib(n):
    # call the function from C
    lib.c_print_fib(n)
