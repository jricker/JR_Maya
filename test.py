import maya.cmds as cmds
mousePos = cmds.autoPlace(um=True)
sl = cmds.ls(selection=True, flatten=True)
x = []
y = []
z = []
pos = []
for i in sl:
    location = cmds.xform(i, query=True, translation=True, worldSpace=True)
    x.append(location[0])
    y.append(location[1])
    z.append(location[2])
avgX = sum(x)/len(x)
avgY = sum(y)/len(y)
avgZ = sum(z)/len(z)
xyzPos = [avgX,avgY,avgZ]
print mousePos
print xyzPos
largestValue = mousePos[0] - xyzPos[0]
positionToUse = 0
for i in range(len(mousePos)):
    if mousePos[i] == 0:
        pass
    else:
        temp = mousePos[i] - xyzPos[0]
        if temp > largestValue:
            largestValue = temp
            positionToUse = i
#print positionToUse
#print mousePos[positionToUse]
#print xyzPos[positionToUse]
if mousePos[positionToUse] - xyzPos[positionToUse] > 0:
    direction = 'positive'
elif  mousePos[positionToUse] - xyzPos[positionToUse] < 0:
    direction = 'negative'
#    
#   
if direction = 'positive':
    if positionToUse == 0:
        for i in range(len(sl)):
            cmds.xform(sl[i], translation=[max(x), y[i], z[i]], worldSpace=True)
    if positionToUse == 1:
        for i in range(len(sl)):
            cmds.xform(sl[i], translation=[x[i], max(y), z[i]], worldSpace=True)
    if positionToUse == 2:
        for i in range(len(sl)):
            cmds.xform(sl[i], translation=[x[i], y[i], max(z)], worldSpace=True)
if direction = 'negative':
    if positionToUse == 0:
        for i in range(len(sl)):
            cmds.xform(sl[i], translation=[min(x), y[i], z[i]], worldSpace=True)
    if positionToUse == 1:
        for i in range(len(sl)):
            cmds.xform(sl[i], translation=[x[i], min(y), z[i]], worldSpace=True)
    if positionToUse == 2:
        for i in range(len(sl)):
            cmds.xform(sl[i], translation=[x[i], y[i], min(z)], worldSpace=True)