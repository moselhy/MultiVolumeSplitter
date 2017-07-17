import os
import dicom
import slicer

class SplitterLogic(object):
	def __init__(self, inputdir):
		self.inputdir = inputdir

	def getDirs(self):
		pathwalk = os.walk(self.inputdir)
		dcmdirs = {}
		for root, dirs, files in pathwalk:
			for file in files:
				if file.lower().endswith(".dcm") or file.lower().endswith(".ima"):
					if root not in dcmdirs:
						dcmdirs[root] = []
					dcmdirs[root].append(file)
		return dcmdirs

	def getVols(self):
		# volumeNumber, (dicomNumber, dicomFile)
		volList = {}
		dcmdirs = getDirs()

		for dcmdir, dcmfiles in dcmdirs.items():
			for file in dcmfiles:
				ds = dicom.read_file(file)
				instanceNumber = ds[0x0020, 0x0013]
				volumeNumber = round()