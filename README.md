# MetaSSN
A Python script suite for generating metanodes and annotation of sequence similarity networks(SSN).  
  
MetaSSN takes a raw data set for an SSN (all by all BLAST results) and condenses the network by clustering sequences with BLAST bitscores above a 'clustering threshold'. Sequences that are clustered together become a 'metanode' (each sequence in a regular SSN is a node, and clustering them creates a 'node made of nodes') in the network. Different metanodes will be connected to each other if members between metanodes share a BLAST bitscore above an 'edge threshold'. The metanode clustering method is inspired from [SSN pipe](https://github.com/ahvdk/SSNpipe).

Where SSN pipe performs the BLAST analysis up to the metanode clustering, MetaSSN starts from the metanode clustering step and provides various ways to add annotations to the network of metanodes. The inclusion of multiple sequences into the same node in a network means that further work is needed to combine and summarize annotations for that metanode. Furthermore, SSN analysis typically requires examination of multiple cut-offs to find the cut-off(s) where the network is appropriately separated for the user's needs. MetaSSN aims to allow the user to collect a single set of annotations and automatically apply these annotations to all networks generated.    
  
There is also an assortment of [Python helper scripts](Python_script_tools) for managing sequence data. These are not required for the function of MetaSSN but are provided for the user's convenience. 
  
# Instructions
For an overview of the usage capabilites of MetaSSN see the [MetaSSN manual](SSN%20Meta%20v4%20manual.pdf).  
  
To get an idea of how MetaSSN can be used as part of the SSN generation and analysis pipeline, see the [MetaSSN tutorial](metaSSN%20tutorial.pdf).
  
The MetaSSN scripts and example files for the tutorial can be downloaded from the [Release](https://github.com/johnchen93/MetaSSN/releases/tag/1.0).  
