# Designed and developed by Jacob Bieker (jacob@bieker.tech)

# Script reads in a csv file containing spiked read counts from TCR sequencing, and calculates the 
# what number is needed to change the counts of each spiked read to the mean. 
# Using the spiked reads, it finds the corresponding VJ region in a MiTCR-formatted CSV file
# It then normalizes the count for each region in the MiTCR file using the multiples from the spikes
#
# Assumptions:
#   1.  A CSV file, named "<MiTCR File>xout.csv" per MiTCR file of the format ID,spike,count
#   2.  A MiTCR csv file per CSV file
#   3.  A CSV file detailing the barcode-to-VJ-region 
#   4.  Spiked reads are supposed to be present in the exact same frequency

#############################################################################
#
#             Setup
#
#############################################################################

#############################################################################
#
#             Spiked Read CSV code
#
#############################################################################

#   identify all .csv files that should be the spiked read counts in the directory 
spiked_files <- list.files(getwd(), pattern = "*_*.txt");
#  Get all the MiTCR files with spiked reads removed in the directory
MiTCR_files <- list.files(getwd(), pattern = "*_*rm.csv");

# Go through each file and read in the CSV spiked_reads, skpping the first line which gives no information
# All operations on the spiked_reads will happen inside the for loop, so that it goes through each file
# and each MiTCR file once
for(spike_file in spiked_files) {
  # Get the corresponding MiTCR file to go with the spiked file
  spiked_file_name <- strsplit(spike_file, ".txt");
  corresponding_MiTCR <- match(paste(spiked_file_name,"rm.csv",sep=""), MiTCR_files)
  
  # Reads in the spiked_read counts
  all_content <- readLines(spike_file)
  skip_second <- all_content[-2]
  spiked_reads <- read.csv(textConnection(skip_second), header = TRUE, stringsAsFactors = FALSE)
  #Get the mean from the last column, which is the read count
  spiked_mean <- mean(spiked_reads[[5]])
  
  # Test vector holding all the multiples needed to hit the mean
  multiples_needed <- spiked_mean/spiked_reads$COUNT
  
  #Puts the spiked_reads in the spiked_reads.frame for later use
  spiked_reads$multiples <- multiples_needed
  
  # Opens the matching MiTCR file, if such file exists
  if(!is.na(MiTCR_files[corresponding_MiTCR])){
  MiTCR_file_data <- read.csv(MiTCR_files[corresponding_MiTCR], stringsAsFactors = FALSE)
  # Get rid of the TRB that is before every V and J segment name, so it can be matched later
  MiTCR_file_data$V.segments <- gsub("^.*?V", "V", MiTCR_file_data$V.segments)
  MiTCR_file_data$J.segments <- gsub("^.*?J", "J", MiTCR_file_data$J.segments)
  
  # Remove the extra characters for the V segments in the spiked counts, so matches occur
  spiked_reads$V <- gsub("-","", spiked_reads$V)
  
  # Empty data.frame to fill with the modified MiTCR data
  MiTCR_output <- data.frame();
  # Go through every row in MiTCR data
    for(index in 1:nrow(spiked_reads)) {
      # Get the row data
      row <- spiked_reads[index,]
      # Subset to a smaller data.frame only those spiked reads that have the same V and J values
      MiTCR_multiple_row <- subset(MiTCR_file_data, row$V == MiTCR_file_data$V.segments & row$J == MiTCR_file_data$J.segments)
      # Point of this whole script, change the sequence count
      MiTCR_multiple_row$Seq..Count <- row$multiples * MiTCR_multiple_row$Seq..Count
      # Then change the percentage by the same amount, as not all counts are changed the same
      MiTCR_multiple_row$Percent <- row$multiples * MiTCR_multiple_row$Percent
      # Add to the data.frame that will be the CSV file
      MiTCR_output <- rbind(MiTCR_output, MiTCR_multiple_row)
    }
  
  # After going through an applying all the multiples, write to CSV file, appending to 
  # original file name, only outputs those rows that match both a V and J segment in spiked_reads
  write.csv(MiTCR_output, file = paste(MiTCR_files[corresponding_MiTCR], sep = "", ".normalized"), quote = FALSE, row.names = FALSE)
  
  }
}
