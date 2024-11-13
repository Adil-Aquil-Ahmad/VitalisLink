import csv


class Donors:
        
    all = []

    def __init__(self, name: str, age: int, blood_group: str, location: str) -> None:

        self.name = name
        self.age = age
        self.__blood_group = blood_group
        self.location = location

        Blood_Groups = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]

        assert blood_group in Blood_Groups, f"{blood_group} is not a valid Blood Group"
        assert age>=18 and age<=60, f"{age}, is not in the permissible age group"

        Donors.all.append(self)
    

    def __str__(self) -> str:

        return f"{self.name}\n \
            {self.age}\n \
            {self.__blood_group}\n \
            {self.location}"


    def __repr__(self) -> str:

        return (
            f"{self.__class__.__name__}({self.name}, {self.age}, "
            f"{self.__blood_group}, {self.location})"
        )
    

    @classmethod
    def instantiate_from_csv(cls):
        cls.all.clear()
        with open('Blood_Collection_Database.csv', 'r') as f:
            reader = csv.DictReader(f)
            people = list(reader)
            
            for donors in people:
                Donors(
                    name = donors.get('name'),
                    age = int(donors.get('age').rstrip()),
                    blood_group = donors.get('blood_group').rstrip(),
                    location = donors.get('location')
                )


    @classmethod
    def instantiate_from_user(cls):
        a = input("Name: ")
        b = int(input("Age: "))
        c = input("Blood Group: ")
        d = input("Location: ")

        with open('Blood_Collection_Database.csv', 'a', newline="") as f:
            writer = csv.writer(f)
            writer.writerow([a, b, c ,d])


# Donors.instantiate_from_user()
Donors.instantiate_from_csv()
# print(Donors.all)