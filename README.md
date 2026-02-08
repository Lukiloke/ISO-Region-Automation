# PROGRAM DESCRIPTION

This is a Python script that automatically finds the ISO3166 (or ISO Region Code) from a ZIP code and a country code. It uses the OpenStreetMap Nominatim and GeoNames databases.

# HOW TO USE

1. Clone this repo to your computer.
2. Prepare a .csv file with your data, as shown in `example.csv` and in the image below.
3. Run the Python program and specify the path (or name, if in the same folder) to your input and output files.
4. Let the program run. Because the APIs used require a minimum delay between each request, I added a 1.1 second delay for every line. Therefore, the program can take some time to process large files.

![Alt Text](image.png "Example Image")

# DEPENDENCIES

To run this script, you will need Python 3 and the following libraries installed on your computer:
```
geopy
pgeocode
sys
csv
time
```

# LICENSING

This project is licensed under the [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html).

If you use **ANY** code from this project:
- You must disclose the source code of your modified work and the source code you used from this project. This means you are not allowed to use code from this project (even partially) in a closed-source project.
- You must state clearly and obviously to all end users that you are using code from this project.
- Your application must also be licensed under the same license.

# DISCLAIMER

This project uses free APIs that are not 100% accurate, so it's possible that some of the results provided are incorrect or that some ISO3166 codes are not found.
If you're looking for highly accurate results, I recommend paying for APIs such as the Google Maps API.
