import random
import maya.cmds as cmds


class CameraShake(object):
    _CONTROL_SUFFIX = '_ShakeControl'
    _GROUP_SUFFIX = '_Shake'
    _SHAKENODES_GROUP = 'SHAKENODES_GROUP'
    _CAMERAS_GROUP = 'CAMERAS_GROUP'

    def __init__(self, camera):
        self._camera = False
        self._control = False
        self._shakeGrp = False
        self._expression = False

        if camera:
            self.setCamera(camera)

    def __str__(self):
        ret = 'CAMERA SHAKE:\n'
        ret += '\tcamera: %s\n' % str(self.camera())
        ret += '\tcontrol: %s\n' % str(self.control())
        ret += '\tshakeGrp: %s\n' % str(self.shakeGrp())
        ret += '\texpression: %s\n' % str(self.expression())
        return ret

    def camera(self):
        return self._camera

    def setCamera(self, camera):
        if cmds.objExists(camera):
            if cmds.objectType(camera, isType='camera'):
                camera = cmds.listRelatives(camera, p=True)[0]
            self._camera = camera
            self.getAssociated()

    def control(self):
        return self._control

    def setControl(self, control):
        self._control = control

    def shakeGrp(self):
        return self._shakeGrp

    def setShakeGrp(self, shakeGrp):
        self._shakeGrp = shakeGrp

    def expression(self):
        return self._expression

    def setExpression(self, expression):
        self._expression = expression

    def selectShakeControl(self):
        if self.control() is not None:
            cmds.select(self.control(), r=True)

    @classmethod
    def toggle(cls):
        """Convenience method to toggle the shake on the selected camera."""
        camera = cmds.ls(sl=True)[0]

        if not cmds.objectType(camera, isType='camera'):
            camera = cmds.listRelatives(camera, c=True)[0]

        if cmds.objectType(camera, isType='camera'):
            csObj = cls(camera)
            status_ = csObj.shakeStatus()

            if status_ == -1:
                csObj.addShake()
                cmds.confirmDialog(title='Info',
                                   icon='information',
                                   message='CameraShake created for:\n' + camera,
                                   button=['Ok'], defaultButton='Ok')
            elif status_ == 0:
                csObj._toggleShakeOn()
                cmds.confirmDialog(title='Info',
                                   icon='information',
                                   message='CameraShake turned on for:\n' + camera,
                                   button=['Ok'], defaultButton='Ok')
            else:
                csObj._toggleShakeOff()
                cmds.confirmDialog(title='Info',
                                   icon='information',
                                   message='CameraShake turned off for:\n' + camera,
                                   button=['Ok'], defaultButton='Ok')
            return True

        msgString = 'Selected object is not a camera.\nPlease select a camera and try again.'
        cmds.confirmDialog(title='Warning',
                           icon='warning',
                           message=msgString,
                           button=['Ok'], defaultButton='Ok')

    def createShakeGroup(self):
        """Make sure the camera shake group exists."""
        if not cmds.objExists(self._CAMERAS_GROUP):
            cmds.group(n=self._CAMERAS_GROUP, empty=True)
            for attr in [c + a for c in 'trs' for a in 'xyz']:
                cmds.setAttr(self._CAMERAS_GROUP + '.' + attr, lock=1)
        if not cmds.objExists(self._SHAKENODES_GROUP):
            cmds.group(n=self._SHAKENODES_GROUP, empty=True)
            for attr in [c + a for c in 'trs' for a in 'xyz']:
                cmds.setAttr(self._SHAKENODES_GROUP + '.' + attr, lock=1)
            cmds.parent(self._SHAKENODES_GROUP, self._CAMERAS_GROUP)

    def cleanShakeGroup(self):
        """See if there are objects in the shake group, delete if not."""
        if cmds.objExists(self._SHAKENODES_GROUP) and \
           cmds.listRelatives(self._SHAKENODES_GROUP, c=True) is None:
            cmds.delete(self._SHAKENODES_GROUP)

            if cmds.objExists(self._CAMERAS_GROUP) and \
               cmds.listRelatives(self._CAMERAS_GROUP, c=True) is None:
                cmds.delete(self._CAMERAS_GROUP)


    def applyCameraLock(self, lock):
        """Set the lock state of the camera. So It cannot accidentally be moved."""
        cam = self.camera()
        if cam is not None:
            for channel in ['t', 'r']:
                for axis in ['x', 'y', 'z']:
                    cmds.setAttr(cam + '.' + channel + axis, lock=lock)

    def getAssociated(self):
        """Retrieve all the associated nodes to the shake."""
        if self.camera() and cmds.attributeQuery('shakeNode', node=self.camera(), exists=True):
            # control
            camConnections = cmds.listConnections(self.camera() + '.shakeNode', s=True, d=False, scn=True)
            if camConnections is not None:
                self.setControl(camConnections[0])

        if self.control():
            # shakeGrp
            shakeConnections = cmds.listConnections(self.control() + '.associatedGrp', s=True, d=False, scn=True)
            if shakeConnections is not None:
                self.setShakeGrp(shakeConnections[0])

            expConnections = cmds.listConnections(self.control() + '.Noise', s=False, d=True, scn=True)
            if expConnections is not None:
                self.setExpression(expConnections[0])

    def _shakeExpression(self, ctrl, target):
        expression_ = ''

        for channel in ['T', 'R']:
            for axis in ['X', 'Y', 'Z']:
                rand = random.randint(0, 9999)  # random seed for each axis
                shake_exp = 'noise((frame * %s.Frequency_%s%s / 100) + %s.Seed_%s + %d) * %s.Amplitude_%s%s / %s' \
                            % (ctrl, channel, axis, ctrl, channel, rand,
                               ctrl, channel, axis, '100' if channel == 'T' else '1')

                jitter_exp = 'noise((frame * 10) + %s.Seed_%s + %d) * %s.Amplitude_%s%s * %s.Jitter_%s / 100' \
                             % (ctrl, channel, rand, ctrl, channel, axis, ctrl, channel)

                final_exp = '((%s) + (%s)) * %s.Noise' % (shake_exp, jitter_exp, ctrl)
                target_attribute = '%s.%s%s' % (target, ('translate' if channel == 'T' else 'rotate'), axis)
                expression_ += '%s = %s;\n' % (target_attribute, final_exp)

        cmds.expression(s=expression_, n='%s_exp' % target)

        self.setExpression('%s_exp' % target)

    def _prepareShakeControl(self):
        """Create the shake control with all the attributes."""
        # create the control
        control = '%s%s' % (self.camera(), self._CONTROL_SUFFIX)
        shakeGrp = '%s%s' % (self.camera(), self._GROUP_SUFFIX)
        if cmds.objExists(control) or cmds.objExists(shakeGrp):
            return

        cmds.spaceLocator(n=control)
        cmds.group(n=shakeGrp, em=True)
        cmds.parent(shakeGrp, control)

        # lock and hide scale
        for at in ['sx', 'sy', 'sz']:
            cmds.setAttr('%s.%s' % (control, at), lock=True, k=False)

        # add the control attributes
        cmds.addAttr(control, ln='NOISE_SWITCH', k=False, at='enum', en='-:')
        cmds.setAttr('%s.NOISE_SWITCH' % control, lock=True, cb=True)
        cmds.addAttr(control, ln='Noise', k=False, at='enum', en='Off:On:')
        cmds.setAttr('%s.Noise' % control, 0, cb=True)

        for channel in ['T', 'R']:
            shakeName = 'TRANSLATION' if channel == 'T' else 'ROTATION'
            cmds.addAttr(control, ln='%s_NOISE' % shakeName, k=False, at='enum', en='-:')
            cmds.setAttr('%s.%s_NOISE' % (control, shakeName), lock=True, cb=True)
            for axis in ['X', 'Y', 'Z']:
                cmds.addAttr(control, ln='Frequency_%s%s' % (channel, axis), k=True, at='double', min=0)
                cmds.addAttr(control, ln='Amplitude_%s%s' % (channel, axis), k=True, at='double', min=0)
            cmds.addAttr(control, ln='Jitter_%s' % channel, k=True, at='double', min=0)
            cmds.addAttr(control, ln='Seed_%s' % channel, k=False, at='short', dv=random.randint(0, 9999))
            cmds.setAttr('%s.Seed_%s' % (control, channel), cb=True)

        # cmds.addAttr(control, ln='CAM_OFFSET', k=False, at='enum', en='-:')
        # cmds.setAttr('%s.CAM_OFFSET' % control, lock=True, cb=True)
        # for axis in ['X', 'Y', 'Z']:
        #     cmds.addAttr(ln='Offset_%s' % axis, k=True, at='double')

        # add message attributes
        cmds.addAttr(control, ln='associatedCam', k=False, at='message')
        cmds.addAttr(control, ln='associatedGrp', k=False, at='message')
        cmds.connectAttr(shakeGrp + '.message', control + '.associatedGrp')

        # add the expression
        self._shakeExpression(control, shakeGrp)

        # register the new nodes to self
        self.setControl(control)
        self.setShakeGrp(shakeGrp)

    def _prepareCamera(self):
        """Add the appropriate attributes to the camera-node"""
        camera = self.camera()
        if not cmds.attributeQuery('cameraLock', node=camera, exists=True):
            cmds.addAttr(camera, ln='cameraLock', at='bool')
        if not cmds.attributeQuery('shakeNode', node=camera, exists=True):
            cmds.addAttr(camera, ln='shakeNode', k=False, at='message')

    def addShake(self):
        """
        Initialize the shake for the camera; create all the
        necessary nodes.
        """
        self._prepareShakeControl()
        self._prepareCamera()

        cmds.connectAttr(self.control() + '.associatedCam', self.camera() + '.shakeNode', force=True)

        self._toggleShakeOn()

    def removeShake(self):
        """Remove the shake completely."""
        self.getAssociated()

        self._toggleShakeOff()

        if self.control() and cmds.objExists(self.control()):
            cmds.delete(self.control())
        if self.shakeGrp() and cmds.objExists(self.shakeGrp()):
            cmds.delete(self.shakeGrp())
        if self.expression() and cmds.objExists(self.expression()):
            cmds.delete(self.expression())
        if cmds.attributeQuery('shakeNode', node=self.camera(), exists=True):
            cmds.deleteAttr(self.camera(), attribute='shakeNode')

        self.setControl(False)
        self.setShakeGrp(False)
        self.setExpression(False)

    def shakeStatus(self):
        """Return the shakeStatus, on/off/doesnt exists."""
        if not self.control() or not cmds.objExists(self.control()):
            return -1
        return cmds.getAttr(self.control() + '.Noise')

    def toggleShake(self):
        """Toggle attach/detach the shake from the camera."""
        current = self.shakeStatus()

        if current == -1:
            self.addShake()
        if current == 0:
            self._toggleShakeOn()
        if current == 1:
            self._toggleShakeOff()

    def _toggleShakeOn(self):
        """Assuming the shake is turned off, turn it on."""
        current = self.shakeStatus()

        if current == 0:
            self.applyCameraLock(False)
            # make sure the shakeControl parent is the same as the camera parent
            camParent = cmds.listRelatives(self.camera(), p=True)
            currParent = cmds.listRelatives(self.control(), p=True)
            if camParent != currParent:
                if camParent is None:
                    cmds.parent(self.control(), w=True)
                else:
                    cmds.parent(self.control(), camParent)

            # copy the rotate order
            cmds.setAttr('%s.ro' % self.control(), cmds.getAttr('%s.ro' % self.camera()))

            # transfer the animation
            channels = [channel + axis for channel in 'tr' for axis in 'xyz']

            for channel in channels:
                connections = cmds.listConnections(self.camera() + '.' + channel,
                                                   scn=True, c=True, p=True, s=True, d=True)
                if connections is None:
                    cmds.setAttr(self.control() + '.' + channel, cmds.getAttr(self.camera() + '.' + channel))
                    connections = []

                for n in range(len(connections) / 2):
                    from_ = connections[n * 2 + 1]
                    to_ = connections[n * 2]

                    cmds.connectAttr(from_, self.control() + '.' + channel)
                    cmds.disconnectAttr(from_, to_)

            # parent the camera under the shakeGrp
            cmds.parent(self.camera(), self.shakeGrp())

            # zero out the transforms

            cmds.setAttr(self.camera() + '.t', 0, 0, 0)
            cmds.setAttr(self.camera() + '.r', 0, 0, 0)

            cmds.setAttr(self.control() + '.Noise', 1)

            # clean up camera shake group if empty
            self.cleanShakeGroup()

            self.applyCameraLock(True)

    def _toggleShakeOff(self):
        """Assuming the shake is turned on, turn it off."""
        current = cmds.getAttr(self.control() + '.Noise')

        if current == 1:
            # make sure the shakenodes group exists
            self.createShakeGroup()

            self.applyCameraLock(False)
            # parent the camera as a sibling of the control
            shakeParent = cmds.listRelatives(self.control(), p=True)
            if shakeParent is not None:
                cmds.parent(self.camera(), shakeParent[0])
            else:
                cmds.parent(self.camera(), w=True)
            cmds.parent(self.control(), self._SHAKENODES_GROUP)

            # copy the rotate order
            cmds.setAttr('%s.ro' % self.camera(), cmds.getAttr('%s.ro' % self.control()))

            # transfer the animation
            channels = [channel + axis for channel in 'tr' for axis in 'xyz']

            for channel in channels:
                connections = cmds.listConnections(self.control() + '.' + channel,
                                                   scn=True, c=True, p=True, s=True, d=True)
                if connections is None:
                    cmds.setAttr(self.camera() + '.' + channel, cmds.getAttr(self.control() + '.' + channel))
                    connections = []

                for n in range(len(connections) / 2):
                    from_ = connections[n * 2 + 1]
                    to_ = connections[n * 2]

                    cmds.connectAttr(from_, self.camera() + '.' + channel)
                    cmds.disconnectAttr(from_, to_)

            cmds.setAttr(self.control() + '.Noise', 0)
            if cmds.objExists(self.camera() + '.cameraLock') and cmds.getAttr(self.camera() + '.cameraLock'):
                self.applyCameraLock(True)