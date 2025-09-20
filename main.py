from pprint import pprint as pp
from trip import *
from stop_finder import *

try:
    with open('api.bin', 'r') as f:
        api_key = f.read()
except FileNotFoundError:
    print("Error: The file 'api.bin' was not found.")
    exit()
except Exception as e:
    print(f"An error occurred while reading the file: {e}")
    exit()


# clean_trip(get_trip(api_key, "208110", "225040"))
# print(clean_trip(get_trip(api_key, "208110", "225040")))
# sf(api_key, "Berowra") # 208110
# sf(api_key, "Gosford") # 225040

def main():
    a = ""
    while True:
        try:
            a = input("Enter Start Location> ")
            start_id = clean_stop(stop_finder(api_key, a))
            a = input("Enter End Location> ")
            end_id = clean_stop(stop_finder(api_key, a))
            print(clean_trip(get_trip(api_key, start_id, end_id))[0])
        except TypeError:
            if a == "quit":
                break
            print("Can't route from/to there!")
    

main()