import os, sys, logging
from splitter import SplitterLogic

sl = SplitterLogic(sys.argv[1], sys.argv[2])

sl.getVols()