# UPS Tracking Number Cracker

I originally wrote this script to try and identify my full UPS tracking number for a preorder. Some folks are able to use UPS My Choice to gain access to this information, but for those who can't, they're limited to seeing the final four digits of their tracking number with minimal tracking information. I decided to share this in case others wanted to do the same.

If you have the shipper number and service-level code of your shipment (which comprise the first eight characters of a UPS tracking number following the '1Z') along with the final four digits, this simple script will narrow down the possible valid tracking numbers and check each of them to see if they are in transit. It's not perfect, but in my case, it narrowed down 10,000 possible combinations to only 32 candidates, which were easy enough to check manually. YMMV, of course.

## Configuring the Script

* Sign up for a free [RapidAPI account](https://rapidapi.com/signup) and get your default [API key](https://rapidapi.com/developer/apps).
* Download `cracker.py` and open it in your IDE or text editor of choice.
* Fill in your RapidAPI key, destination country, first eight characters of the tracking number following the '1Z', and last four digits. This can be done by updating the values of the variables on lines 12 - 23 of the script.
  * If you don't know the first eight characters of the tracking number, find someone who's expecting an order from the same shipper and knows their tracking number. If they're willing to share the first eight characters of their tracking number, there's a good likelihood it may be yours too.
  * If you don't know the last four digits of your tracking number, use UPS's '[Track by Reference Number](https://www.ups.com/track)' feature. Sometimes, you can locate the last four digits by using your phone number or order number as a reference, depending on the shipper.
* Save and run the script.

Via command line:
```shell
$ python3 /path/to/cracker.py
```

This is by no means perfect (I wrote it in about half an hour, so it doesn't have any sort of error handling.) Just thought I'd make the tool available in care others were interested.
