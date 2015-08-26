# !/usr/local/bin/python

__author__ = 'Jacob Bieker'

'''BARCODE GENERATOR
    BY Luca Comai and Tyson Howell
    December 2009

    Updated by Jacob Bieker 2015'''

print '\n\nBARCODE GENERATOR by LC and TH\n\t--***---\nPlant Biology and Genome Center\n\tUC Davis\nUpdated by Jacob Bieker <jacob@bieker.tech>\n'
print '''This program generates barcodes
of a desired length, distance, and GC content
The primer sequences currently used
are the illumina paired end primers\n'''


# ___________________________________________________raw input

import math

print 'Enter LENGTH as an integer (i.e. 4)'

# ask the desired number of bases in barcode
length = int(raw_input("Barcode length: "))

print '\nEnter the number of barcodes (default is LENGTH x 5)'

# ask how many barcodes should be made
number = raw_input("Total number of barcodes: ")
if number == '':
    number = length * 5
else:
    number = int(number)

print '\nEnter the minimum number of different bases between barcodes (default is LENGTH/2, i.e. 7->3, 4->2)'

# ask what is the least number of bases that must be different
# between any two barcodes
diffs = raw_input("Min. no. of different bases between barcodes: ")
if diffs == '':
    diffs = length // 2
else:
    diffs = int(diffs)

print '\nEnter desired GC content range in percentages (i.e. 50 ->50%)'

# ask for desired GC content range
mingc = raw_input("Minimum GC content (default is 0):")
if mingc == '':
    mingc = 0
else:
    mingc = float(mingc) / 100

maxgc = raw_input("Maximum GC content (default is 100):")
if maxgc == '':
    maxgc = 100
else:
    maxgc = float(maxgc) / 100

print 'Go through every permutation of base pairs, or choose random codes? \n Note: Random codes are usually faster,' \
      ' but every permutation guarantees every possibility tried'

boolean_random = raw_input('Random Codes? (Y/n): ')

if boolean_random.lower() in ("y", "yes", "yeah", "si", "ja"):
    boolean_random = True
elif boolean_random == '':
    boolean_random = True
else:
    boolean_random = False

# If True, the number of attempts has to be specified, else try every possibility
if boolean_random:
    print '\nThe default number of random codes to test is 1000. \n Do not enter more than a million'

    # ask what is the maximum number of random codes to be tested
    attempts = raw_input('How many attempts?:')
    if attempts == '':
        # Gets the maximum number of possibilities based on 4 bp
        attempts = 1000
    else:
        attempts = int(attempts)
else:
    attempts = 4**length

# ___________________________________________________process

# make list of the four bases
gene_bases = ['a', 'c', 'g', 't']

# intialize string to hold all characters necessary for permutations to work
gene_permutation_list = ""

# Add 1 for each number, to be incremented to track changes
for j in range(length):
    gene_permutation_list += "acgt"

#Now create ever ypossibility for the the bp length
import itertools
all_permutations = itertools.permutations(gene_permutation_list, length)
# Keep track of location in all permutation list
all_permutations_loc = 0

# initialze the barcode list
barcode_list = []

# initialize the first barcode
first_barcode = []

# prime the tested list, for future counting
tested = []

# function to determine GC content
def gc_cont(bar_code):
    gc = 0.0
    for base in range(length):
        if bar_code[base] == 'c' or bar_code[base] == 'g':
            gc += 1
        else:
            gc += 0
    cont = gc / length
    return cont

# import random module
import random

# make the first barcode
# add first barcode to barcode list. This is needed for the
# first comparison of "compare_barcode" function
while not barcode_list:
    for i in range(length):
        first_barcode.append(random.choice(gene_bases))
    if maxgc >= gc_cont(first_barcode) >= mingc:
        barcode_list.append(first_barcode)
    else:
        first_barcode = []

# the barcode "cradle": a place where each barcode will sit
barcode = []

# ___________________________________________________define functions

# function makes the barcode
def make_barcode(length):
    global barcode
    # empties the barcode cradle
    barcode = []
    for i in range(length):
        barcode.append(random.choice(gene_bases))

# Alternative that goes through possibilites one by one
# Slower in most cases, but will hit every possibility
def make_barcode_slow(all_permutations):
    global barcode
    global all_permutations_loc
    #empties the barcode cradle
    barcode = []
    # Get the list in the permutation list
    specific_permutation = all_permutations.next()
    all_permutations_loc += 1
    for i in range(length):
        barcode.append(specific_permutation[i])
        print(all_permutations_loc)


# barcode is tested vs the previously generated barcodes
def compare_barcode(length, barcode_l):
    count = 0
    global barcode
    if boolean_random:
        # run barcode creator
        make_barcode(length)
    else:
        # run the slow barcode creator
        make_barcode_slow(all_permutations=all_permutations)
        # keep track of it
    tested.append(barcode)
    # testing of barcode
    if barcode not in barcode_list:
        global count_list
        count_list = []
        # compare to barcodes in list
        for bc in barcode_l:
            # matches to existing barcodes
            # are scored as points
            count = 0
            for pos in range(length):
                if barcode[pos] == bc[pos]:
                    count += 1
                else:
                    count += 0
            # for each barcode a list of scores is made
            count_list.append(count)
        # if the barcode has enough unique bases
        # and the proper GC content, it is added
        # to the list of good barcodes
        if max(count_list) > length - diffs:
            count_list = []
        elif gc_cont(barcode) <= maxgc and gc_cont(barcode) >= mingc:
            barcode_list.append(barcode)
            count_list = []
        else:
            count_list = []
    else:
        pass

import csv
def check_existing(csv_file, barcodes):
    # Goes through the generate barcodes and sees if they contain an already existing barcode
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
    for barcode in barcodes:
        complete_barcode = ''
        for base_pair in barcode:
            complete_barcode+=base_pair
        for existing in existing_barcode_list:
            if existing.lower() in complete_barcode.lower():
                barcodes.remove(barcode)
                print("Removing Barcode: ")
                print(barcode)
            else:
                continue

num_of_existing = 0
def get_num_of_existing(csv_file):
    with open(csv_file, 'r') as csvfile:
        contents = csv.reader(csvfile)
        headers = contents.next()
        for line in contents:
            global num_of_existing
            num_of_existing = line[0]

def write_existing(csv_file, barcodes):
    # Get the current last number of barcodes
    global num_of_existing
    # Assume that not changing between the last use and this one
    with open(csv_file, 'a') as csvfile:
        for barcode in barcodes:
            num_of_existing = str(int(num_of_existing) + 1)
            complete_barcode = ''
            for base_pair in barcode:
                complete_barcode+=str(base_pair)
            csvfile.write('\n' + str(num_of_existing) + "," + str(complete_barcode))

# ___________________________________________________run functions

# initialize count

count_list = []

import os
if os.path.isfile("existing_barcodes.csv"):
    # If going through every possiblity, don't stop until have enough barcodes
    if boolean_random:
        # program stalls if too many attempts are allowed
        # and few barcodes remain to be discovered
        # this loop keeps the attempts within the range allowed
        while len(tested) < attempts:
            if len(barcode_list) < number:
                compare_barcode(length, barcode_list)
                # Checks if any barcodes are in the existing_barcodes file
                check_existing("existing_barcodes.csv", barcode_list)
            else:
                break
    else:
        while len(barcode_list) < number:
            compare_barcode(length, barcode_list)
            # Checks if any barcodes are in the existing_barcodes file
            check_existing("existing_barcodes.csv", barcode_list)
else:
    if boolean_random:
        # program stalls if too many attempts are allowed
        # and few barcodes remain to be discovered
        # this loop keeps the attempts within the range allowed
        while len(tested) < attempts:
            if len(barcode_list) < number:
                compare_barcode(length, barcode_list)
    else:
        while len(barcode_list) < number:
            compare_barcode(length, barcode_list)

barcode_list.sort()

print "\n\nRESULTS\n\ngood barcodes and GC content:"

for i in barcode_list:
    print i, int(gc_cont(i) * 100), '%'

print '\nnumber of tested barcodes:'

print len(tested)

print '\nnumber of good barcodes:'

print len(barcode_list)

# count base composition in each of the barcode position
from collections import defaultdict

print '\nbase compositions by position'

for pos in range(length):
    list_l = [i[pos] for i in barcode_list]
    base_count = defaultdict(int)
    for base in list_l:
        base_count[base] += 1
    print base_count.keys(), base_count.values()

# ___________________________________________________manipulate barcodes and print results

# But the correct barcodes into the exisitng barcodes filefor later runs
get_num_of_existing('existing_barcodes.csv')
write_existing('existing_barcodes.csv', barcode_list)
# make a file for the barcoded primer sequence
# open file
barfile = open('barcode.txt', 'a')

print >> barfile, 'These are the barcodes of length ' + str(length) + ' with a distance of ' + str(diffs) + ' bases\n'

# ___________________________________________________primer sequence

# modify the primer as desired. This seq is the
# illumina PE primer
primerA = 'AGATCGGAAGAGCGGTTCAGCAGGAATGCCGAG'

# note that the adapter is originally as below
# GATCGGAAGAGCGGTTCAGCAGGAATGCCGAG
# however, an A is added to allow the sequencing
# primer to anneal

# this is the complementary primer from illumina
# same for regular or PE
primerB = 'ACACTCTTTCCCTACACGACGCTCTTCCGATCT'

# the output will be:
# >adA2_cccca
# ccccaAGATCGGAAGAGCTCGTATGCCGTCTTCTGCTTG
# >adB2_cccca
# ACACTCTTTCCCTACACGACGCTCTTCCGATCTtggggT
# note that barcode is in lower case

# define adapter names
name_rootA = '>adA2_'

name_rootB = '>adB2_'

# initialize a holder name for the complement of barcode
comp_barcode = ''

# define function to derive complement of any seq
# try/except/finally is to make sure that the 'maketrans'
# has been imported
def reverse_comp(seq):
    try:
        maketrans
    except NameError:
        from string import maketrans
    finally:
        comp_table = maketrans('actg', 'tgac')
        global comp_barcode
        comp_barcode = seq[::-1].translate(comp_table)


for i in barcode_list:
    j = ''.join(i)
    reverse_comp(j)
    print >> barfile, '%s%s\n%s%s\n%s%s\n%s%sT\n\n' % (name_rootA, j, j, primerA, name_rootB, j, primerB, comp_barcode)

print '''\nA file called barcode.txt has been generated.
It contains the adapter sequences with each
barcode in lower case\n\n'''

# close file or it does not get updated
barfile.close()

# ___________________________________________________log

# changes from 2.7:
# rephrase raw input queries
# default barcodes to test to 10,000
# clean up shell results
