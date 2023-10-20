# Jose Landa
# Student ID: 000999884
# C950 - WGUPS Package Delivery Routing

import csv
import datetime
from truck import Truck
from createHashTable import MyChainingHashTable
from package import Package

# this will read the data inside the package csv file
with open("CSVFiles/PackageCSVFile.csv") as csv_package_file:
    Package_CSV_File = list(csv.reader(csv_package_file, delimiter=","))

# this will read the data inside the address csv file
with open("CSVFiles/AddressCSVFile.csv") as csv_address_file:
    Address_CSV_File = list(csv.reader(csv_address_file, delimiter=","))

# this will read the data inside the distance csv file
with open("CSVFiles/DistanceCSVFile.csv") as csv_distance_file:
    Distance_CSV_File = list(csv.reader(csv_distance_file, delimiter=","))


# this function uses the package class to create package objects
# then the information for each package object is loaded into a package hash table
def load_package_information(file_name, package_list_table):
    with open(file_name) as package_data:
        package_info = csv.reader(package_data)
        for package in package_info:
            package_id = int(package[0])
            package_address = package[1]
            package_city = package[2]
            package_state = package[3]
            package_zip = package[4]
            package_deadline = package[5]
            package_weight = package[6]
            package_status = "Package At Hub Location Awaiting Departure"

            p = Package(package_id, package_address, package_city, package_state,
                        package_zip, package_deadline, package_weight, package_status)

            package_list_table.insert(package_id, p)


# this function is used to find the distance between two separate addresses
def distance_from(x_value, y_value):
    distance = Distance_CSV_File[x_value][y_value]
    if distance == '':
        distance = Distance_CSV_File[y_value][x_value]

    return float(distance)


# this function is used to retrieve the address information from the address string
def get_address(package_address):
    for row in Address_CSV_File:
        if package_address in row[2]:
            return int(row[0])


# this next section is for manually loading packages onto each truck. By manually loading
# the trucks, this allows for greater control of which packages go together and
# of the special requirements for each package

# this is the first truck being manually loaded with packages
first_truck = Truck(16, 18, [1, 13, 14, 15, 16, 19, 20, 21, 29, 30, 31, 34, 37, 39, 40], 0.0,
                    "4001 South 700 East", datetime.timedelta(hours=8))


# this is the second truck being manually loaded with packages (removed 25 and 26 from packages d/t error)
second_truck = Truck(16, 18, [3, 6, 18, 25, 26, 28, 32, 33, 36, 38], 0.0,
                     "4001 South 700 East", datetime.timedelta(hours=9, minutes=10))


# this is the third truck being manually loaded with packages
third_truck = Truck(16, 18, [2, 4, 5, 7, 8, 9, 10, 11, 12, 17, 22, 23, 24, 27, 35], 0.0, "4001 South 700 East",
                    datetime.timedelta(hours=10, minutes=30))


# this creates the hash table using the createHashTable class
package_table = MyChainingHashTable()


# this section loads packages into the hash table created above
load_package_information("CSVFiles/PackageCSVFile.csv", package_table)


# this function will order the packages to be delivered onto a truck using the
# nearest neighbor algorithm.
# the function will calculate the distance driven by each truck.
def package_delivery_system(delivery_truck):
    # this section will place all packages into an array stating that they are not yet delivered
    undelivered = []
    for pid in delivery_truck.packages:
        package = package_table.find(pid)
        undelivered.append(package)

    # this section will clear the list of packages so that the packages can be placed into the
    # truck using the nearest neighbor algorithm for optimal placement.
    delivery_truck.packages.clear()

    # this section will go through the list of packages that have not been delivered until
    # the list is completely empty.
    # the next nearest package will be added to the truck one by one.
    while len(undelivered) > 0:
        next_address = 2000
        next_package = None
        for package in undelivered:
            if distance_from(get_address(delivery_truck.address), get_address(package.package_address)) <= next_address:
                next_address = distance_from(get_address(delivery_truck.address), get_address(package.package_address))
                next_package = package

        # this section adds the nearest package into the truck
        delivery_truck.packages.append(next_package.package_id)

        # this section removes the package that was added to the truck from the list of undelivered packages
        undelivered.remove(next_package)

        # this section adds up the amount of miles that were driven by the truck to the current delivery address
        delivery_truck.miles += next_address

        # this section updates the trucks address to the next package to be delivered
        delivery_truck.address = next_package.package_address

        # this section updates the time the departure and delivery times of packages within the truck
        delivery_truck.time += datetime.timedelta(hours=next_address / 18)
        next_package.time_delivered = delivery_truck.time
        next_package.time_departed = delivery_truck.time_of_departure


# this section runs the trucks through the process of loading and delivering packages with
# the delivery algorithm created above.
package_delivery_system(first_truck)

package_delivery_system(second_truck)

# this section checks to see if either the first_truck or second_truck has returned before
# the third_truck is allowed to depart.
third_truck.time_of_departure = min(first_truck.time, second_truck.time)
package_delivery_system(third_truck)


class Main:
    total_miles_traveled = str(first_truck.miles + second_truck.miles + third_truck.miles)
    # the user interface will be created in this section, allowing the user to check the total miles driven,
    # the package delivery status, package departure status, and the time the package was delivered.

    print("Western Governor's University Parcel Service - WGUPS")
    print("Route total mileage: " + total_miles_traveled)
    user_input = input("To check status of a package, please type 'STATUS', or type 'END' to close program. ")

    # if the user types the word STATUS, they will then be prompted to enter a time in HH:MM:SS format. Once a time is
    # input by the user, the user is then prompted to either check the status of a single package, or to check the
    # status of all packages at the input time. Any invalid entries will prompt an error message to print, and will
    # close the application.
    if user_input.lower() == "status":
        try:
            input_time = input("Please enter a specific time to check package status. Please enter the time "
                               "in the following format: HH:MM:SS ")
            (h, m, s) = input_time.split(":")
            convert_time = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))

            single_or_all_input = input("To view the status of only one package, please type 'ONE'. To see the status"
                                        " of all packages, please type 'ALL'. ")

            # this section will print the status of a single package based on the package id input by the user.
            if single_or_all_input.lower() == "one":
                try:
                    check_one_package = input("Please enter the package ID number: ")
                    package = package_table.find(int(check_one_package))
                    package.status_update(convert_time)
                    print(str(package))
                except ValueError:
                    print("Invalid entry. Please restart application")
                    exit()

            # this section will print the status of all packages at the specified time.
            elif single_or_all_input.lower() == "all":
                try:
                    for pid in range(1, 41):
                        package = package_table.find(pid)
                        package.status_update(convert_time)
                        print(str(package))
                except ValueError:
                    print("Invalid entry. Please restart application.")
                    exit()
            else:
                print("Entry invalid. Please restart application.")
                exit()
        except ValueError:
            print("Invalid entry. Please restart application.")
            exit()

    # this section will close the application if the user inputs 'END' in the prompt.
    elif user_input == "END":
        print("Thank you for using WGUPS.")
        exit()

    # this section will close the application if an invalid entry is made by the user.
    else:
        print("Invalid input. Please restart application.")
        exit()
