# LabKey-Oncotator-Tool
Java files for the integration of Oncotator with LabKey, the file should be a part of the SequenceAnalysis module,
they are broken out here for ease of seperation.

# How To Use
Run oncotator_install script on first run to download and install the required components.  Note that you may need to first change users to install the tools.
Pass either a VCF or MAF file to Oncotator in LabKey, the output will either be TCGAMAF (default), VCF, or a TSV file.

The Broad's instructions for installing and running Oncotator are here:  http://gatkforums.broadinstitute.org/discussion/4154/howto-install-and-run-oncotator-for-the-first-time

# Process of Integrating New Tools into LabKey

1. Modify the oncotator_install script to download and run the installation of the tool
2. In many cases, modify OncotatorWrapper to run the tool's default command line options
3. Modify OncotatorAnalysis to run the UI and give the proper command line option args to the wrapper to be executed
4. Copt the contents of oncotator_install into
C:\labkey\externalModules\labModules\SequenceAnalysis\pipeline_code\sequence_tools_install.sh so it is executed as part
of installing the SequenceAnalysis pipeline.

