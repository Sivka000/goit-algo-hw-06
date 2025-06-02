from collections import UserDict
import re

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

#Збереження імен контакту
class Name(Field):
    def __init__(self, value):
        super().__init__(value)

#Збереження номерів телефону
class Phone(Field):
    def __init__(self, value):
        if not self.validate(value):
            raise ValueError("Phone number must be 10 digits.")
        super().__init__(value)
    
    #Статичний метод для перевірки формату номера телефону.
    @staticmethod 
    def validate(value):
        return bool(re.fullmatch(r'\d{10}', value))

#Зберігання інформації про контакт.
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    #Додає новий номер телефону.
    def add_phone(self, phone_number):
        phone = Phone(phone_number)
        self.phones.append(phone)

    #Видаляє номер телефону зі списку.
    def remove_phone(self, phone_number):
        phone_to_remove = self.find_phone(phone_number)
        if phone_to_remove:
            self.phones.remove(phone_to_remove)
        else:
            raise ValueError("Phone number not found.")
        
    #Змінює старий номер телефону на новий.
    def edit_phone(self, old_number, new_number):
        phone_to_edit = self.find_phone(old_number)
        if phone_to_edit:
            self.remove_phone(old_number)
            self.add_phone(new_number)
        else:
            raise ValueError("Old phone number not found.")
        
    #Пошук
    def find_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None

    def __str__(self):
        phones_str = '; '.join(p.value for p in self.phones) if self.phones else "No phones"
        return f"Contact name: {self.name.value}, phones: {phones_str}"
    
#Адресна книга
class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
        else:
            raise KeyError

    def __str__(self):
        if not self.data:
            return "Address book is empty."
        return "\n".join(str(record) for record in self.data.values())


book = AddressBook()
john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")
book.add_record(john_record)
jane_record = Record("Jane")
jane_record.add_phone("9876543210")
book.add_record(jane_record)
print(book)
john = book.find("John")
john.edit_phone("1234567890", "1112223333")
print(john)
found_phone = john.find_phone("5555555555")
print(f"{john.name}: {found_phone}")

book.delete("Jane")