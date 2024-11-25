import csv


class Donors:
        
    all = []
    new = []

    def __init__(self, first_name: str, middle_name: str, last_name: str, age: int, blood_group: str, address: str, city: str, state: str, pin_code: int, latitude: float, longitude: float, status: str) -> None:

        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.age = age
        self.__blood_group = blood_group
        self.address = address
        self.city = city
        self.state = state
        self.pin_code = pin_code
        self.latitude = latitude
        self.longitude = longitude
        self.status = status

        Blood_Groups = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]

        assert blood_group in Blood_Groups, f"{blood_group} is not a valid Blood Group"
        assert age>=18 and age<=60, f"{age}, is not in the permissible age group"
        assert pin_code>=100000 and pin_code<=999999, f"{pin_code}, is not a valid pin code"

        Donors.all.append(self)
        if self.status=="Confirmed":
            Donors.new.append(self)

    def __str__(self) -> str:

        return f"{self.first_name}\n \
            {self.middle_name}\n \
            {self.last_name}\n \
            {self.age}\n \
            {self.__blood_group}\n \
            {self.address}\n \
            {self.city}\n \
            {self.state}\n \
            {self.pin_code}\n \
            {self.latitude}\n \
            {self.longitude}\n \
            {self.status}"


    def __repr__(self) -> str:

        return (
            f"{self.__class__.__name__}({self.first_name}, {self.middle_name}, {self.last_name}, "
            f"{self.age}, {self.__blood_group}, {self.address}, {self.city}, {self.state}, {self.pin_code})"
            f"{self.latitude}, {self.longitude}, {self.status}"
        )
    

    @classmethod
    def instantiate_from_csv(cls, CSV_File_Name):
        cls.all.clear()
        with open(CSV_File_Name, 'r') as f:
            reader = csv.DictReader(f)
            people = list(reader)
            
            for donors in people:
                try:
                    Donors(
                        first_name=donors.get('First Name'),
                        middle_name=donors.get('Middle Name'),
                        last_name=donors.get('Last Name'),
                        age=int(donors.get('Age').strip()),
                        blood_group=donors.get('Blood Group').strip(),
                        address=donors.get('Address'),
                        city=donors.get('City'),
                        state=donors.get('State'),
                        pin_code=int(donors.get('Pin Code')),
                        latitude=float(donors.get('Latitude')),
                        longitude=float(donors.get('Longitude')),
                        status=donors.get('Status')
                    )
                except (AssertionError, ValueError) as e:

                    print(f"Skipping invalid record: {donors}. Reason: {e}")
                


    @classmethod
    def instantiate_from_admin(cls, CSV_File_Name, Username):
        with open(CSV_File_Name, 'r') as f:
            reader = csv.DictReader(f)
            people = list(reader)
            
            for donors in people:
                first_name=donors.get('First Name')
                middle_name=donors.get('Middle Name')
                last_name=donors.get('Last Name')
                age=int(donors.get('Age').strip())
                blood_group=donors.get('Blood Group').strip()
                address=donors.get('Address')
                city=donors.get('City')
                state=donors.get('State')
                pin_code=int(donors.get('Pin Code'))
                latitude=float(donors.get('Latitude'))
                longitude=float(donors.get('Longitude'))
                status=donors.get('Status')
                with open('Blood_Collection_Database.csv', 'a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([Username, first_name, middle_name, last_name, age, blood_group, address, city, state, pin_code, latitude, longitude, status])




# Donors.instantiate_from_user()
# Donors.instantiate_from_csv()
# print(Donors.all)