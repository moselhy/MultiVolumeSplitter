import os, sys, logging, shutil

if len(sys.argv) < 2:
	raise IOError("No path was given")
	exit(1)

pathwalk = os.walk(sys.argv[1])
alldcms = []

for root, dirs, files in pathwalk:
	for file in files:
		if file.lower().endswith(".dcm"):
			alldcms.append(root)
alldcms = set(list(alldcms))


outputDir = os.path.expanduser("~\\Documents\\Temp\\NrrdOutput")
if os.path.exists(outputDir):
	shutil.rmtree(outputDir)
os.makedirs(outputDir)

nrrds = []
sequence = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLSequenceNode")


i = 0
for dcmdir in alldcms:
	dirname = os.path.split(dcmdir)[1]
	cwd = os.path.dirname(os.path.realpath(__file__))
	volumePath = os.path.join(outputDir, dirname + ".nrrd")
	nrrds.append(volumePath)
	execString = os.path.join(cwd, "runner.bat") + " " + os.path.join(cwd, "DicomToNrrdConverter.exe") + " --inputDicomDirectory " + dcmdir + " --outputVolume " + volumePath
	os.system(execString)
	volNode = slicer.util.loadVolume(volumePath, returnNode=True)[1]
	sequence.SetDataNodeAtValue(volNode, str(i))
	slicer.mrmlScene.RemoveNode(volNode)
	i+=1
# Start editing with low battery

