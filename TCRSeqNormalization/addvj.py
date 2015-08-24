from os import path
import argparse

def parse_vj(vjpath):
    spikedict = {}
    vjfile = open(vjpath)
    vjli=[]
    for line in vjfile:
        vjli.append(line.strip())
    vjfile.close()
    for i, line in enumerate(vjli):
        if '[' in line:
            spikeid = line.split('[')[1].split(']')[0] # assumes ACTAAGC[DMxxx]CGTA format
            spikeid=''.join([char for char in spikeid if char.isdigit()])
            if not spikeid in spikedict:
                spikedict[spikeid]=vjli[i-1].split()
    return spikedict
        
def parse_spikes(path):
    """
    parse_spikes: read the spikes from the spike configuration file into a list
    Arguments: path - the path to the spike configuration file
    Returns: spikeli - the list containing all spikes in the following format: (SPIKE_ID,SPIKE)
    """
    spikeli = []
    with open(path) as spikefile: 
        for line in spikefile:
            vals=line.split()
            spikeli.append((vals[0],vals[1]))
    return spikeli
    
def modify_spikes(spikepath, spikedict, spikeli):
    path = spikepath.split('.')
    newpath = path[0]+'vj.'+path[1]
    newfile = open(newpath, 'w')
    
    for spike in spikeli:
        curid = ''.join([char for char in spike[0] if char.isdigit()])
        newline = list(spike)+spikedict[curid]
        newfile.write(' '.join(newline)+'\n')
        
    newfile.close()
        
def main():
    parser = argparse.ArgumentParser(description='Get inputs for the FASTQ modifying script.') # set arguments
    parser.add_argument('spikes', help = 'The file containing spike data.')
    parser.add_argument('vjfile', help = 'The directory to be modified.')
    args=parser.parse_args()
    
    assert (path.exists(args.spikes) and path.exists(args.vjfile))

    spikeli = parse_spikes(args.spikes) # get the list of spikes
    spikedict = parse_vj(args.vjfile) # get the dict of vj values for each spike   
    modify_spikes(args.spikes,spikedict,spikeli)

if __name__=='__main__':
    main()