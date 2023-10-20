class Truck:
    def __init__(self, capacity, speed, packages, miles, address, time_of_departure):
        self.capacity = capacity
        self.speed = speed
        self.packages = packages
        self.miles = miles
        self.address = address
        self.time_of_departure = time_of_departure
        self.time = time_of_departure

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s" % (self.capacity, self.speed, self.packages, self.miles, self.address,
                                           self.time_of_departure)
