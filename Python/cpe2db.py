import sqlite3
import xml.etree.cElementTree as ET
import pathlib
import requests, zipfile, io


def vendorProductsearch(root):
        """
        """
        master = []
        for cpe in root.iter(r'{http://scap.nist.gov/schema/cpe-extension/2.3}cpe23-item'):
            elements = cpe.attrib['name'].split(':')
            s = elements[3:6]
            s.append(cpe.attrib['name'])
            master.append(tuple(s))

        return master

r = requests.get('https://nvd.nist.gov/feeds/xml/cpe/dictionary/official-cpe-dictionary_v2.3.xml.zip')
z = zipfile.ZipFile(io.BytesIO(r.content))
z.extractall(pathlib.Path().cwd())

# Connect to database
conn = sqlite3.connect('nist.db')

# Create a cursor
c = conn.cursor()

# Create a table
c.execute("""CREATE TABLE cpe_data (
      vendor TEXT,
      product TEXT,
      version TEXT,
      cpe TEXT
      )""")

# datatypes: NULL, INTEGER, REAL, TEXT, BLOB

# Commit our command
conn.commit()

# Parse XML
tree = ET.parse(pathlib.Path.cwd() / "official-cpe-dictionary_v2.3.xml")
root = tree.getroot()
values = vendorProductsearch(root)

# Populate database
c.executemany("INSERT INTO cpe_data VALUES (?,?,?,?)",values)

# Commit our command
conn.commit()

# Close our connection
conn.close()

# import matching algorithm
# # Connect to database
# conn = sqlite3.connect('nist.db')
# # Set the cursor
# c = conn.cursor()
# # Select all CPEs with a fuzzy match to the query
# c.execute("SELECT * FROM cpe_data")
# all_records = c.fetchall()
# # Use a list comprehension to filter approximate matches
# fuzzy_matches = my_fuzz_function()
# for record in fuzzy_matches:
#     print(record)
