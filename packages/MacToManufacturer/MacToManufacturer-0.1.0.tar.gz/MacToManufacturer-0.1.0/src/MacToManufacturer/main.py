import csv
import pkg_resources

class MacToMan():

    def __init__(self) -> None:

        # Load CSV file from local storage.
        stream = pkg_resources.resource_stream(__name__, 'data/manuf.csv').read().decode().splitlines()
        self.csv_file = csv.reader(stream)

    def search(self, macaddress) -> str:
        """
        This method searches for macaddress in CSV file
        & returns value.
        """

        # Get only the first 3 octlets of macaddress.
        macaddr = macaddress[:8].replace("-",":")

        # Search the csv file.
        for row in self.csv_file:
            #if current rows 2nd value is equal to input, print that row
            if macaddr == row[0] or macaddr.upper() == row[0]:
                return row[1]

        return None