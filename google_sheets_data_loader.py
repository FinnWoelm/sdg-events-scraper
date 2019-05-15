import csv
import urllib2

class GoogleSheetsDataLoader:

    def __init__(self, id, tab):
        self.id     = id
        self.tab    = tab

    # Converts the Google sheet into a JSON-like dictionary
    def to_dictionary(self):
        reader = csv.DictReader(self.to_csv())

        lines = []
        for row in reader:
            lines.append(row)

        return lines

    # Converts the Google sheet to CSV
    def to_csv(self):
        return urllib2.urlopen(self.csv_url())

    # Return the URL for exporting the sheet as CSV
    def csv_url(self):
        return (self.url() + "export?format=csv" +
                "&id=" + self.id +
                "&gid=" + self.tab)

    # Return the URL of the sheet
    def url(self):
        return "https://docs.google.com/spreadsheets/d/" + self.id + "/"
