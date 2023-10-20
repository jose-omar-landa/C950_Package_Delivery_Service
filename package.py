
class Package:
    def __init__(self, package_id, address, city, state, package_zip, delivery_deadline, weight, delivery_status):
        self.package_id = package_id
        self.package_address = address
        self.city = city
        self.state = state
        self.zip = package_zip
        self.delivery_deadline = delivery_deadline
        self.weight = weight
        self.delivery_status = delivery_status
        self.time_departed = None
        self.time_delivered = None

    def __str__(self):
        return "Package ID: %s, Address: %s, %s, %s, %s, Delivery Deadline: %s, Package Weight: %s kg, " \
               "Time Delivered: %s, Status: %s" % (self.package_id, self.package_address, self.city, self.state,
                                                   self.zip, self.delivery_deadline, self.weight, self.time_delivered,
                                                   self.delivery_status)

    def status_update(self, convert_time):
        if self.time_delivered < convert_time:
            self.delivery_status = "Package Delivered"
        elif self.time_departed > convert_time:
            self.delivery_status = "Package En Route To Destination"
        else:
            self.delivery_status = "Package At Hub Location Awaiting Departure"
