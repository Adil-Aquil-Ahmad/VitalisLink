import csv


class Person:
        
    all = []

    def __init__(self, name: str, age: int, blood_group: str, location: str) -> None:

        self.name = name
        self.age = age
        self.__blood_group = blood_group
        self.location = location

        Blood_Groups = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]

        assert blood_group in Blood_Groups, f"{blood_group} is not a valid Blood Group"
        assert age>=18 and age<=60, f"{age}, is not in the permissible age group"

        Person.all.append(self)
    

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

        with open('Blood_Group_Database.csv', 'r') as f:
            reader = csv.DictReader(f)
            people = list(reader)
            
            for person in people:
                Person(
                    name = person.get('name'),
                    age = int(person.get('age').rstrip()),
                    blood_group = person.get('blood_group').rstrip(),
                    location = person.get('location')
                )


    @classmethod
    def instantiate_from_user(cls):
        a = input("Name: ")
        b = int(input("Age: "))
        c = input("Blood Group: ")
        d = input("Location: ")

        with open('Blood_Group_Database.csv', 'a', newline="") as f:
            writer = csv.writer(f)
            # if Person("Adil", 19, "A+", "placeholder") not in Person.all:
            writer.writerow([a, b, c ,d])

Person.instantiate_from_user()
Person.instantiate_from_csv()
print(Person.all)
