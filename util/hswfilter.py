class HsvFilter:

    def __init__(self, hMin=0, sMin=0, vMin=0, hMax=0, sMax=0, vMax=0,
                 sAdd=0, sSub=0, vAdd=0, vSub=0, cannyOn=0, cannyKernel=0, cannyRatio=0, maxThreshold=0, lowThreshold=0,
                 blurOn=0, blurKernel=0):
        self.hMin = hMin
        self.sMin = sMin
        self.vMin = vMin
        self.hMax = hMax
        self.sMax = sMax
        self.vMax = vMax
        self.sAdd = sAdd
        self.sSub = sSub
        self.vAdd = vAdd
        self.vSub = vSub
        self.cannyOn = cannyOn
        self.cannyKernel = cannyKernel
        self.cannyRatio = cannyRatio
        self.maxThreshold = maxThreshold
        self.lowThreshold = lowThreshold
        self.blurOn = blurOn
        self.blurKernel = blurKernel
