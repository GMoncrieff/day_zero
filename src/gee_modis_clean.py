import ee

def getQABits(image, start, end, newName):
  # Compute the bits we need to extract.
  pattern = 0
  for i in range(start, end):
     pattern += pow(2, i)
  return image.select([0], [newName]).bitwiseAnd(pattern).rightShift(start)

def updateMultipleMask(index, areaMask):
  def updateMaskInner(image):
    # Select the QA band
    QA = image.select('DetailedQA')
    ndlim = image.select([index]).gt(0)

    # Get the cloud_state bits and find cloudy areas.
    cloud = getQABits(QA, 0, 1, 'cloud_state')\
      .expression("b(0) == 2 || b(0) == 3")

    landWaterFlag = getQABits(QA, 11, 13, 'land_water_flag')

    # Create a mask that filters out deep ocean and cloudy areas.
    mask = landWaterFlag.eq(1)\
      .And(cloud.Not())\
      .And(areaMask.select(['flag']).eq(1))\
      .And(ndlim.gt(0))

    return image.updateMask(mask)
  return updateMaskInner