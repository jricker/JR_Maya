#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# CamNoiseTool by David Alonso #
# alodavid.com                 #
# 2013                         #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#





from pymel import core as pc
import random
from functools import partial


#
# CamNoiseTool main class
#
class CamNoiseTool():
    _UI_WINDOW_NAME = 'noisetoolwindow'
    _CONTROL_SUFIX = '_noisecontrol'
    _GROUP_SUFIX = '_noise'
    _ASSOCIATED_CAM_ATTRIBUTE_NAME = 'associated_cam'
    
    # Constructor method
    def __init__(self, cam=False):
        if cam:
            self.camera = str(cam)
            self.control = self.getControlLocator()

    # Returns the name of the noise control locator, empty string is there's none
    def getControlLocator(self):
        try:
            parent = pc.listRelatives(self.camera, p=True)[0]
            control_locator = pc.listRelatives(parent, p=True)[0]
        except:
            control_locator = ''
        return control_locator

    # Creates locator named [basename] with attributes for noise controlling
    def createNoiseControl(self):
        # Create locator
        control = '%s%s'%(self.camera, self._CONTROL_SUFIX)
        pc.spaceLocator(n=control)
        # Create attribute for turning noise on/off
        pc.addAttr(ln='NOISE_SWITCH', k=False, at='enum', en='-:')
        pc.setAttr('%s.NOISE_SWITCH'%control, lock=True, cb=True)
        pc.addAttr(ln='Noise', k=False, at='enum', en='Off:On:')
        pc.setAttr('%s.Noise'%control, 1, cb=True)
        # Create translation noise attributes: frequency, amplitude (x, y, z), jitter and seed
        for noise_type in ['T', 'R']:
            nname = 'TRANSLATION' if noise_type == 'T' else 'ROTATION'
            pc.addAttr(ln='%s_NOISE'%nname, k=False, at='enum', en='-:')
            pc.setAttr('%s.%s_NOISE'%(control, nname), lock=True, cb=True)
            for axis in ['X', 'Y', 'Z']:
                pc.addAttr(ln='Frequency_%s%s'%(noise_type, axis), k=True, at='double', min=0)
                pc.addAttr(ln='Amplitude_%s%s'%(noise_type, axis), k=True, at='double', min=0)
            pc.addAttr(ln='Jitter_%s'%noise_type, k=True, at='double', min=0)
            pc.addAttr(ln='Seed_%s'%noise_type, k=False, at='short', dv=random.randint(0, 9999))
            pc.setAttr('%s.Seed_%s'%(control, noise_type), cb=True)
        # Create extra attributes for camera position offset
        pc.addAttr(ln='CAM_OFFSET', k=False, at='enum', en='-:')
        pc.setAttr('%s.CAM_OFFSET'%control, lock=True, cb=True)
        for axis in ['X', 'Y', 'Z']:
            pc.addAttr(ln='Offset_%s'%axis, k=True, at='double')
        return control

    # Copies rotation order from object [src] to object [dst]
    def copyRotateOrder(self, src, dst):
        pc.setAttr('%s.rotateOrder'%dst, pc.getAttr('%s.rotateOrder'%src))
    
    # Creates noise expressions for each translation/rotation animation curve
    def createNoiseExpressions(self):
        # Loop over translation (T) and rotation (R)
        expression_text = ''
        for noise_type in ['T', 'R']:
            # Loop over three axes
            for axis in ['X', 'Y', 'Z']:
                rand = random.randint(0, 9999) # random seed for each axis
                noise_exp = 'noise((frame * %s.Frequency_%s%s / 100) + %s.Seed_%s + %d) * %s.Amplitude_%s%s / %s' %(self.control, noise_type, axis, self.control, noise_type, rand, self.control, noise_type, axis, '100' if noise_type == 'T' else '1')
                jitter_exp = 'noise((frame * 10) + %s.Seed_%s + %d) * %s.Amplitude_%s%s * %s.Jitter_%s / 100' %(self.control, noise_type, rand, self.control, noise_type, axis, self.control, noise_type)
                final_exp = '((%s) + (%s)) * %s.Noise' %(noise_exp, jitter_exp, self.control)
                target_attribute = '%s.%s%s' %(self.target, ('translate' if noise_type == 'T' else 'rotate'), axis)
                expression_text += '%s = %s;\n' %(target_attribute, final_exp)
        pc.expression(s=expression_text, n='%s_exp'%self.target)

    # Connects noise control offset attributes with translation attributes of the camera
    def connectOffsetAttributes(self):
        for axis in ['X', 'Y', 'Z']:
            pc.connectAttr('%s.Offset_%s' %(self.control, axis), '%s.translate%s' %(self.camera, axis))

    # Disconnects noise control offset attributes with translation attributes of the camera
    def disconnectOffsetAttributes(self):
        for axis in ['X', 'Y', 'Z']:
            pc.disconnectAttr('%s.Offset_%s' %(self.control, axis), '%s.translate%s' %(self.camera, axis))

    # Connect all animated transform curves from object [src] to object [dst]. Copy the values of non-animated attributes
    def reconnectAnimationCurves(self, src, dst):
        for transform in ['translate', 'rotate']:
            for axis in ['X', 'Y', 'Z']:
                # If attribute has a connection (anim curve) means it's animated
                src_attr = '%s.%s%s'%(src, transform, axis)
                dst_attr = '%s.%s%s'%(dst, transform, axis)
                if pc.connectionInfo(src_attr, id=True):
                    conn = pc.connectionInfo(src_attr, sfd=True)
                    pc.connectAttr(conn, dst_attr)
                    pc.disconnectAttr(conn, src_attr)
                else:
                    pc.setAttr(dst_attr, pc.getAttr(src_attr))

    # Sets transforms to zero for [obj]
    def zeroTransforms(self, obj):
        pc.rotate(obj, a=True, xyz=0)
        pc.move(obj, a=True, xyz=0)

    # Creates camera groups and parents the orginal camera to them
    def createNoiseHierarchy(self):
        # Reset camera position and rotation
        self.zeroTransforms(self.camera)
        # Group camera
        target = pc.group(self.camera, n='%s_noise'%self.camera)
        # Parent camera to locator
        pc.parent(target, self.control)
        # Reset group transforms to 0
        self.zeroTransforms(target)
        return target
        
    # Adds noise attributes to selected camera
    def addNoise(self, cmd=''):
        # Create locator with noise attributes
        self.control = self.createNoiseControl()
        # Copy rotation order from cam to locator
        self.copyRotateOrder(self.camera, self.control)
        # Move all camera transform attributes to locator
        self.reconnectAnimationCurves(self.camera, self.control)
        # 
        self.target = self.createNoiseHierarchy()
        # Create noise expressions and connect them to control and target camera group. 
        self.createNoiseExpressions()
        # Connect translation offset attributes
        self.connectOffsetAttributes()
        # Select noise control
        pc.select(self.control)
        self.closeUI()
    
    # Disconnects current noise locator from camera
    def disconnectNoise(self, cmd=''):
        # Parent camera to world
        pc.parent(self.camera, w=True)
        # Disconnect offset attributes and move the anim curves back to the camera
        self.disconnectOffsetAttributes()
        self.reconnectAnimationCurves(self.control, self.camera)
        # Add an extra attribute to the control locator to remember which camera was associated with. Then hide it
        self.addControlLinkedCameraAttribute()
        pc.hide(self.control)
        pc.select(self.camera)
        self.closeUI()
    
    # Connects back the locator control previously used to the associated camera
    def reapplyNoise(self, cmd=''):
        self.control = self.getAssociatedLocator()
        pc.showHidden(self.control)
        self.reconnectAnimationCurves(self.camera, self.control)
        target = pc.listRelatives(self.control, c=True, typ='transform')[0]
        pc.parent(self.camera, target)
        self.zeroTransforms(self.camera)
        self.connectOffsetAttributes()
        pc.select(self.control)
        self.closeUI()

    # Returns array with all noise control nodes existing in the scene
    def getNoiseControls(self):
        controls = []
        for o in pc.ls(typ='locator'):
            loc = pc.listRelatives(o, p=True)[0]
            attribute = '%s.%s'%(loc, self._ASSOCIATED_CAM_ATTRIBUTE_NAME)
            if pc.objExists(attribute):
                controls.append(loc)
        return controls
    
    # Returns the camera under the hierarchy of [control], False if none found
    def getCameraUnderControl(self, control):
        for o in pc.listRelatives(control, ad=True, s=True):
            if pc.objectType(o) == 'camera':
                return pc.listRelatives(o, p=True)[0]
        return False
    
    # Adds extra attribute to the control locator so it remembers the camera associated to
    def addControlLinkedCameraAttribute(self):
        # If attribute does not exist yet, create it
        attribute = '%s.%s'%(self.control, self._ASSOCIATED_CAM_ATTRIBUTE_NAME)
        if not pc.objExists(attribute):
            pc.addAttr(self.control, ln=self._ASSOCIATED_CAM_ATTRIBUTE_NAME, dt='string')
        pc.setAttr(attribute, self.camera)
    
    # Renames all control locator linked camera attributes to the new camera name they are linked to
    def renameLinkedCameraAttributes(self):
        for loc in self.getNoiseControls():
            c = self.getCameraUnderControl(loc)
            pc.setAttr('%s.%s'%(loc, self._ASSOCIATED_CAM_ATTRIBUTE_NAME), c)
    
    # Returns associated locator for camera. False if no one found
    def getAssociatedLocator(self):
        # Cycle through locators in the scene, searching for the ones with associated camera attribute, and matching that attribute against the camera name
        for loc in pc.ls(typ='locator'):
            loc = pc.listRelatives(loc, p=True)[0] #get transform node from shape
            attribute = '%s.%s'%(loc, self._ASSOCIATED_CAM_ATTRIBUTE_NAME)
            if pc.objExists(attribute):
                if pc.getAttr(attribute) == self.camera:
                    return loc
        return False
    
    # Returns True if camera has noise already applied, False otherwise
    def cameraHasNoiseApplied(self):
        if self.control:
            if pc.objExists('%s.Seed_T'%self.control) and pc.objExists('%s.Seed_R'%self.control): #check any 2 noise attributes
                noise_status = True
            else:
                noise_status = False
        else:
            noise_status = False
        return noise_status

    # Returns True if there's a noise locator that controlled the camera noise but was disconnected, False otherwise
    def cameraHasPreviousNoise(self):
        return True if self.getAssociatedLocator() else False
    
    # Returns the current noise status for the camera => 0: no noise available, 1: noise currently applied, 2: noise previously applied (disconnected)
    def getCameraNoiseStatus(self):
        if self.cameraHasNoiseApplied(): #camera has noise applied
            return 1
        elif self.cameraHasPreviousNoise(): #camera had noise applied but was disconnected
            return 2
        else: #no noise applied so far
            return 0
 
    # Opens tool's main window
    def showUI(self):
        if pc.window(self._UI_WINDOW_NAME, q=True, exists=True):
            pc.deleteUI(self._UI_WINDOW_NAME, wnd=True)
        win = pc.window(self._UI_WINDOW_NAME, title='Cam noise tool', w=150, h=100, s=False)
        form = pc.formLayout()
        # Create UI buttons depending on current camera noise status
        status = self.getCameraNoiseStatus()
        if status == 0:
            b = pc.button(l='Add noise', w=140, h=40, c=partial(self.addNoise))
        elif status == 1:
            b = pc.button(l='Remove noise', w=140, h=40, c=partial(self.disconnectNoise))
        else:
            b = pc.button(l='Reapply noise', w=140, h=40, c=partial(self.reapplyNoise))
        pc.formLayout(form, e=True, attachForm=[(b, 'top', 10), (b, 'left', 10), (b, 'right', 10), (b, 'bottom', 10)])
        pc.showWindow(win)

    # Closes tool's main window
    def closeUI(self):
        pc.deleteUI(self._UI_WINDOW_NAME, wnd=True)


#
# Main function called from the menu
#
def run():
    # Get selected camera
    sel = pc.ls(sl=True, ca=True, dag=True)
    if len(sel) < 1:
        pc.confirmDialog(t='Select a camera', m='Please, select a camera to apply the noise on.', b='OK')
        return
    else:
        cam = pc.listRelatives(sel[0], p=True)[0]
        cn = CamNoiseTool(cam)
        cn.showUI()