__author__ = 'Jacob Bieker'


barcodes = ['ATCACGTA', 'TATCACGA', 'TAATCACG', 'TTAGGCTA', 'TGCATGCA', 'CACGTA']

def check_existing(csv_file, barcodes):
    # Goes through the generate barcodes and sees if they contain an already existing barcode
    import csv
    existing_barcode_list = []
    with open(csv_file, 'r') as csvfile:
        existing_codes = csv.reader(csvfile)
        headers = existing_codes.next()
        for row in existing_codes:
            # Go through and get each barcode and add to list
            # Assumes that barcodes will be located in the second row
            existing_barcode_list.append(row[1])

    # Now go through the barcodes and see if the list is contained within any of them
    # Remove those that do contain an existing barcode
    # Adds to to_remove list, as to not skip any barcodes
    barcodes_to_remove = []
    for barcode in barcodes:
        for existing in existing_barcode_list:
            if existing.lower() in barcode.lower():
                barcodes_to_remove.append(barcode)
                print("Removing Barcode: ")
                print(barcode)
            else:
                continue
    # Actually remove the barcode
    for item_to_remove in barcodes_to_remove:
        barcodes.remove(item_to_remove)

import csv
num_of_existing = 0
def get_num_of_existing(csv_file):
    with open(csv_file, 'r') as csvfile:
        contents = csv.reader(csvfile)
        headers = contents.next()
        for line in contents:
            global num_of_existing
            num_of_existing = line[0]
            print(num_of_existing)

def write_existing(csv_file, barcodes):
    # Get the current last number of barcodes
    global num_of_existing
    # Assume that not changing between the last use and this one
    num_of_existing += 1
    with open(csv_file, 'a') as csvfile:
        for barcode in barcodes:
            csvfile.write(str(num_of_existing) + "," + str(barcode))

check_existing('existing_barcodes.csv', barcodes)
get_num_of_existing('existing_barcodes.csv')
write_existing('existing_barcodes.csv', barcodes)