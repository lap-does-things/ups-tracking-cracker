import requests
import json
from itertools import product

'''
BEGIN CONFIGURATION VARIABLES, COMPLETE THE DETAILS BELOW WITH YOUR OWN INFO
'''

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Paste a RapidAPI Application Key between the '' below
RAPIDAPI_KEY = ''

# Type the destination country below
DESTINATION_COUNTRY = 'United States'

# Type the shipper number and service code below
# (These are the first eight characters following the 1Z of a tracking number)
FIRST_EIGHT_OF_TRACKING = '00000000'

# Type the last four known digits of your tracking number
# (This can be found by using the UPS 'Track by Reference' feature
LAST_FOUR_OF_TRACKING = '0000'

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

'''
END CONFIGURATION VARIABLES, DON'T MAKE CHANGES BELOW UNLESS YOU KNOW WHAT YOU'RE DOING
'''


# Integer values for all possible characters of a tracking number
CHAR_VALUES = {
    '0': '0', '1': '1', '2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7', '8': '8', '9': '9', 'A': '2',
    'B': '3', 'C': '4', 'D': '5', 'E': '6', 'F': '7', 'G': '8', 'H': '9', 'I': '0', 'J': '1', 'K': '2', 'L': '3',
    'M': '4', 'N': '5', 'O': '6', 'P': '7', 'Q': '8', 'R': '9', 'S': '0', 'T': '1', 'U': '2', 'V': '3', 'W': '4',
    'X': '5', 'Y': '6', 'Z': '7'
}

# All possible missing digits from '0000' through '9999'
POSSIBLE_ID_PREFIXES = [''.join(prefix) for prefix in product('0123456789', repeat=4)]

# API configuration
API_URL = 'https://order-tracking.p.rapidapi.com/trackings/realtime'
API_HEADERS = {
    'content-type': 'application/json',
    'x-rapidapi-host': 'order-tracking.p.rapidapi.com',
    'x-rapidapi-key': RAPIDAPI_KEY
}


def test_tracking_number(tracking_number):
    """
    Queries the tracking API to determine if a tracking number is active
    :param tracking_number: String value of
    :return: Boolean indicating tracking number is active and matches DESTINATION_COUNTRY
    """
    request = f'{{"tracking_number": "{tracking_number}", "carrier_code": "ups"}}'
    response = requests.request("POST", API_URL, data=request, headers=API_HEADERS)
    j = json.loads(response.text)
    return j['data']['items'][0]['status'] != 'notfound' \
           and j['data']['items'][0]['destination_country'] == DESTINATION_COUNTRY


def get_valid_tracking_numbers(shipper_number, service_code, known_id_suffix, checksum):
    """
    Uses the known tracking details to generate all possible valid UPS tracking numbers
    :param shipper_number: Characters 3-8 of a tracking number
    :param service_code: Characters 9-10 of a tracking number
    :param known_id_suffix: Digits 15-17 of a tracking number (first 3 of final four)
    :param checksum: Final digit of tracking number
    :return: List of all valid tracking numbers matching the provided parameters
    """
    valid_tracking_numbers = list()

    for prefix in POSSIBLE_ID_PREFIXES:
        experimental_tracking_number = f'1Z{shipper_number}{service_code}{prefix}{known_id_suffix}{checksum}'
        if is_valid_tracking(experimental_tracking_number):
            valid_tracking_numbers.append(experimental_tracking_number)

    return valid_tracking_numbers


def is_valid_tracking(tracking_number):
    """
    Determines if a tracking number is a valid UPS tracking number using its checksum
    :param tracking_number: String value of a tracking number
    :return: Boolean indicating if the tracking number is valid
    """
    converted = ''.join([CHAR_VALUES[ch] for ch in tracking_number])[2:17]
    checksum = tracking_number[17]

    tracking_number_digits = [int(ch) for ch in converted]

    sum_1 = 0
    for i in range(0, len(tracking_number_digits), 2):
        sum_1 += tracking_number_digits[i]

    sum_2 = 0
    for i in range(1, len(tracking_number_digits), 2):
        sum_2 += tracking_number_digits[i]
    sum_2 *= 2

    comb_sum = sum_1 + sum_2
    exp_checksum = (10 - comb_sum % 10) % 10

    return exp_checksum == int(checksum)


def main():
    """
    Generates all potential valid tracking numbers and queries an API to find active ones
    :return: None
    """
    params = {
        'shipper_number': FIRST_EIGHT_OF_TRACKING[:6],
        'service_code': FIRST_EIGHT_OF_TRACKING[6:8],
        'known_id_suffix': LAST_FOUR_OF_TRACKING[:3],
        'checksum': LAST_FOUR_OF_TRACKING[3]
    }
    print('FINDING POSSIBLE TRACKING NUMBERS... (THIS MAY TAKE A BIT)\n')
    found = 0
    tracking_numbers = get_valid_tracking_numbers(**params)
    for tracking_number in tracking_numbers:
        if test_tracking_number(tracking_number):
            found += 1
            print(tracking_number)
    print(f'\nCOMPLETE! FOUND {found} POTENTIAL TRACKING NUMBERS.')


if __name__ == '__main__':
    main()
