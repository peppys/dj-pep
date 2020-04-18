import csv
import phonenumbers
from phonenumbers import PhoneNumber

from lib.firestore.client import find_contact, add_contact


def parse_number(phone_number: str) -> PhoneNumber:
    return phonenumbers.parse(phone_number, keep_raw_input=True, region='US')


def is_valid_phone_number(phone_number: str) -> bool:
    try:
        number = parse_number(phone_number)

        return phonenumbers.is_valid_number(number)
    except Exception:
        return False


with open('contacts.csv', 'r') as csvfile:
    data = csv.reader(csvfile)

    imported = 0
    for row in data:
        first_name = row[2]
        potential_phone_numbers = row[6:17]

        valid_phone_numbers = [phone_number for phone_number in potential_phone_numbers if
                               is_valid_phone_number(phone_number)]

        if len(valid_phone_numbers) == 0:
            continue

        phone_number_obj = parse_number(valid_phone_numbers[0])
        formatted_phone_number = phonenumbers.format_number(phone_number_obj,
                                                            phonenumbers.PhoneNumberFormat.E164)

        existing_contact = find_contact(formatted_phone_number)
        if existing_contact:
            continue

        add_contact(phone_number=formatted_phone_number, name=first_name)
        imported += 1

        if imported % 10 == 0:
            print(f'Imported {imported} contacts...')

    print(f'Finished importing {imported} contacts.')
