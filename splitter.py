from shutil import copyfile
import os
import dicom
import slicer

class SplitterLogic(object):
	def __init__(self, inputdir, exportdir):
		self.inputdir = inputdir
		self.exportdir = exportdir

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
		# volumeNumber, [(dicomNumber, dicomFile)]
		volList = {}
		dcmdirs = self.getDirs()

		for dcmdir, dcmfiles in dcmdirs.items():
			print("dcmfiles: " + str(len()))
			for filename in dcmfiles:
				file = os.path.join(dcmdir, filename)
				print("processing " + file)
				ds = dicom.read_file(file)
				instanceNumber = int(ds[0x0020, 0x0013].value)
				print("instance number: " + str(instanceNumber))
				imagesInAquisition = int(ds[0x0020, 0x1002].value)
				slicesPerVol = int(ds[0x0021, 0x104f].value)
				totalVolumes = imagesInAquisition / slicesPerVol
				volumeNumber = int(instanceNumber / slicesPerVol) + 1
				print("volumeNumber is " + str(volumeNumber))
				dicomNumber = int(ds[0x0020, 0x9057].value)
				if volumeNumber not in volList:
					volList[volumeNumber] = []
				volList[volumeNumber].append((dicomNumber, file))

		for vol, dcmList in volList.items():
			print("Copying volume " + str(vol))
			folderPath = os.path.join(self.exportdir, str(vol))
			if not os.path.exists(folderPath):
				os.makedirs(folderPath)
			for dcmNumber, dcmFile in dcmList:
				dest = os.path.join(folderPath, str(dcmNumber) + ".dcm")
				print("Copying dcm to " + dest)
				if os.path.exists(dest):
					os.remove(dest)
				copyfile(dcmFile, dest)
