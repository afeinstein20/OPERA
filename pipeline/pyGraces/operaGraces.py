#!/opt/anaconda/bin/python
# -*- coding: iso-8859-1 -*-
"""
    *** IMPORTANT NOTE ***
    Use line below as shebang for default python location
    #!/usr/bin/python
    
    Use a line similar to the ones below as shebang for custom python location
    #!/$HOME/Ureka/variants/common/bin/python
    #!/opt/anaconda/bin/python

    Created on May 28 2015

    Description: A wrapper to run Opera GRACES reduction pipeline.
    
    @author: Eder Martioli <emartioli@lna.br>
    
    Laboratorio Nacional de Astrofisica, Brazil.
    
    Simple usage example:
    
    .../opera-1.0/pipeline/pyGraces/operaGraces.py --datarootdir=/data/GRACES/
    --pipelinehomedir=.../opera-1.0/ --productrootdir=.../Reductions/GRACES/
    --night=20140506 --product="CALIB" -pvts
"""

__version__ = "1.0"

__copyright__ = """
    Copyright (c) ...  All rights reserved.
    """

from optparse import OptionParser
import sys,os
import gracespipeline
import graces

parser = OptionParser()
parser.add_option("-N", "--night", dest="night", help="night directory",type='string',default="")
parser.add_option("-D", "--datarootdir", dest="datarootdir", help="data root directory",type='string',default="/data/GRACES/")
parser.add_option("-O", "--pipelinehomedir", dest="pipelinehomedir", help="pipeline directory",type='string',default="/Users/edermartioli/opera-1.0/")
parser.add_option("-P", "--productrootdir", dest="productrootdir", help="data product root directory",type='string',default="/Users/edermartioli/Reductions/GRACES/")
parser.add_option("-T", "--product", dest="product", help='target product: "CALIBRATIONS", "OBJECTS" (default)"',type='string',default="OBJECTS")
parser.add_option("-a", action="store_true", dest="cleanall", help="JUST clean all products",default=False)
parser.add_option("-c", action="store_true", dest="clean", help="clean products",default=False)
parser.add_option("-s", action="store_true", dest="simulate", help="simulate",default=False)
parser.add_option("-p", "--plot", action="store_true", dest="plot", help="plots",default=False)
parser.add_option("-v", "--verbose", action="store_true", dest="verbose", help="verbose",default=False)
parser.add_option("-t", "--trace", action="store_true", dest="trace", help="trace",default=False)

try:
    options,args = parser.parse_args(sys.argv[1:])
except:
    print "Error: check usage with operaGraces.py -h ";sys.exit(1);

if options.verbose:
    print 'PIPELINE HOME DIR: ', options.pipelinehomedir
    print 'DATA ROOT DIR: ', options.datarootdir
    print 'PRODUCT ROOT DIR: ', options.productrootdir
    print 'NIGHT: ', options.night

"""
Set up directories:
"""
Dirs = graces.Directories(options.pipelinehomedir,options.datarootdir,options.productrootdir,options.night)

"""
Set up config files:
"""
config = graces.ConfigFiles(Dirs)

"""
Set up GRACES keywords:
"""
keywords = graces.Keywords()

"""
Set up modes available for reduction:
"""
allowanyreadout = False

forcecalibration = False # This is set to "True" for calibrations even when there is no object files
if(options.product == "CALIBRATIONS") :
    forcecalibration = True

modes = graces.ReductionModes(Dirs, keywords, allowanyreadout, forcecalibration)

modes.displayOverallStats()

for mode in modes.getInstReadModes() :
    intrumentmode = mode[0]
    readoutspeed = mode[1]
    modes.displayModeStats(intrumentmode,readoutspeed)
    input = [options.night,intrumentmode,readoutspeed,options.clean,options.simulate,options.plot,options.verbose,options.trace,allowanyreadout,options.product,options.cleanall]
    gracespipeline.executePipeline(input, Dirs, config, keywords)

modes.cleanModes()



