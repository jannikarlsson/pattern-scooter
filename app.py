import functions
import argparse

parser = argparse.ArgumentParser(description='For parsing scooter deets')
parser.add_argument('--id', nargs='?', default=0, const=0)
parser.add_argument('--user', nargs='?', default=0, const=0)
parser.add_argument('--runtime', nargs='?', default=0, const=0)
parser.add_argument('--delay', nargs='?', default=0, const=0)
args = parser.parse_args()

# Checks if there is an input argument
inp = args.id
user = args.user
runtime = int(args.runtime)
delay = int(args.delay)

# If there is no input, user is prompted for one and shown menu to use the client manually
if inp == 0 or user == 0:
    if inp == 0:
        inp = input('Enter id: ')
    if user == 0:
        user = int(input('Enter user id: '))
    # Run with menu
    functions.simulate(inp, user, runtime, 0, 1)
else:
    # Run simulation
    functions.simulate(inp, user, runtime, delay, 0)