#          Designed and Developed by Jacob Bieker (jacob@bieker.us)
#     
#       This script is designed to created plots of genomics data for the 
#       Brenden-Colson Center and Stand Up 2 Cancer. 
#
#       Assumptions:
#       - Average is taken by t_alt_count/(t_alt_count+t_ref_count)
#
##############################################################################
#
#                 Setup
#
##############################################################################
# Check if libraries are installed, if not, install them
require(Cairo)
require(plotrix)
##############################################################################
#
#                 End Setup
#
##############################################################################

#Split data into tumor data and metastasis data
tumor_data <- labkey.data[ with(labkey.data,  grepl("T_tumor", sample)  & !is.na(labkey.data$sample) ) , ]
metastasis_data <- labkey.data[ with(labkey.data,  grepl("M_tumor", sample)  & !is.na(labkey.data$sample) ) , ]

# Get percentages
average_t <- tumor_data$t_alt_count / (tumor_data$t_alt_count + tumor_data$t_ref_count);
#Add average back in so we can sort later to get right names
tumor_data <- cbind(tumor_data, average_t);
#Sort from biggest to smallest
average_t <- sort(average_t, decreasing = TRUE);

#Switch order of variants around to match sorted averages
tumor_data <- tumor_data[match(average_t, tumor_data$average_t),];

# Getting the labels to put on the plots
t_labels <- c();
t_variants <- tumor_data$gene;

for (t_variant in t_variants) {
  t_parts <- strsplit(t_variant, "[:;(]");
  t_labels <-c(t_labels, unique(rapply(t_parts, function(x) head(x, 1))))
}

#Get percentages
average_m <- metastasis_data$t_alt_count / (metastasis_data$t_alt_count + metastasis_data$t_ref_count);
#Add average back in so we can sort later to get right names
metastasis_data <- cbind(metastasis_data, average_m);
#Sort from biggest to smallest
average_m <- sort(average_m, decreasing = TRUE);

#Switch order of variants around to match sorted averages
metastasis_data <- metastasis_data[match(average_m, metastasis_data$average_m),];

# Getting the labels to put on the plots
m_labels <- c();
m_variants <- metastasis_data$gene;

for (m_variant in m_variants) {
  m_parts <- strsplit(m_variant, "[:;(]");
  m_labels <-c(m_labels, unique(rapply(m_parts, function(x) head(x, 1))))
}

##################################################
#
#           Graphing bar plot data
#
##################################################                                   

# First, check if one or the other of the data.frames is null, and skip parts that need that if so

# Checks if the appropriate data.frame is not empty, give boolean which determines what graphs
# created and displayed
is_m <- !(is.data.frame(metastasis_data) & nrow(metastasis_data)==0)
is_t <- !(is.data.frame(tumor_data) & nrow(tumor_data)==0)

if (is_t == TRUE) {
  #   Open a Cairo device to take your plotting output:
  Cairo(file="${imgout:Primary_barplot.png}", type="png");
  #  Plot:
  barplot(average_t, ylab= "Variant Frequency", names.arg=t_labels, axis.lty=3, space=0.5, cex.names=0.8, las=3, main="Primary Tumor");
  dev.off();
}

if (is_m == TRUE) {
  #   Open a Cairo device to take your plotting output:
  Cairo(file="${imgout:Metastasis_barplot.png}", type="png");
  #  Plot:
  barplot(average_m, ylab= "Variant Frequency", names.arg=m_labels, axis.lty=3, space=0.5, cex.names=0.8, las=3, main="Metastisis Tumor");
  dev.off();
}
# Start creation of tumor vs metastasis plot. Main problem is having to make both vectors the same length
# Plan: Start with creating a single row data.frame with all the Tumor ones. Then, go through the column names in that data.frame, checking whether the column names from Metastasis exist or not, if not, add the column with a 0, if so, do nothing. Repeat for other one. Sort both alphabetically to make sure they line up correctly, then scatter plot it.

if (((is_m == TRUE) & (is_t == TRUE))) {
  #Adds all primary tumor labels and values to the data.frame
  tumor_data.frame <- data.frame(default = 0);
  for( i in 1:length(t_labels)) {
    tumor_data.frame[, t_labels[i]] <- average_t[i];
  }
  
  # Now add the metastasis ones that do not exist in the tumor part
  for ( i in 1:length(m_labels)) {
    if (m_labels[i] %in% colnames(tumor_data.frame)) {
      print("Overlap");
    } else {
      # If it exits in metastasis and not tumor, then tumor has a 0 for the mutation
      tumor_data.frame[, m_labels[i]] <- 0;
    }
  }
  
  print(tumor_data.frame);
  
  #Same thing, now for metastasis first
  #TODO: Make this a function
  #Adds all primary metastasis labels and values to the data.frame
  metastasis_data.frame <- data.frame(default = 0);
  for( i in 1:length(m_labels)) {
    metastasis_data.frame[, m_labels[i]] <- average_m[i];
  }
  
  # Now add the tumor ones that do not exist in the metastasis part
  for ( i in 1:length(t_labels)) {
    if (t_labels[i] %in% colnames(metastasis_data.frame)) {
      print("Overlap");
    } else {
      # If it exits in tumor and not metastasis, then metastasis has a 0 for the mutation
      metastasis_data.frame[, t_labels[i]] <- 0;
    }
  }
  print(metastasis_data.frame);
  
  # Remove default column to reduce to only the data
  metastasis_data.frame[, "default"] <- NULL
  tumor_data.frame[, "default"] <- NULL
  #Sort both so the order is the same and the points line up, not really matter the order
  metastasis_data.frame <- metastasis_data.frame[,order(names(metastasis_data.frame))]
  tumor_data.frame <- tumor_data.frame[,order(names(tumor_data.frame))]
  
  #Convert points to vector to be plotted
  tumor_scatterplot.data <- as.numeric(as.vector(tumor_data.frame[1,]))
  metastasis_scatterplot.data <- as.numeric(as.vector(metastasis_data.frame[1,]))
  
  
  #   Open a Cairo device to take your plotting output:
  Cairo(file="${imgout:Primary_Metastasis.png}", type="png");
  par(pty="s") 
  #  Plot:
  sizeplot(jitter(tumor_scatterplot.data), jitter(metastasis_scatterplot.data), bg="red", pch=23, col="black", powscale=TRUE, scale=0.7, xlim=c(0:1), ylim=c(0:1), ylab= "Metastasis", xlab = "Primary", main="Primary vs Metastasis Mutations");
  abline(0,1, lty=3);
  dev.off();
}