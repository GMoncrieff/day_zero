import ee
import math
# Function to add a time band.
def addDependents(image):
  # Compute time in fractional years since the epoch.
  years = image.date().difference('1970-01-01', 'year')
  timeRadians = ee.Image(years.multiply(2 * math.pi)).rename('t')
  constant = ee.Image(1)
  return image.addBands(constant).addBands(timeRadians.float())


# Function to compute the specified number of harmonics
# and add them as bands.  Assumes the time band is present.
def addHarmonics(freqs,cosNames,sinNames):
  def addHarmonicsInner(image):
    # Make an image of frequencies.
    frequencies = ee.Image.constant(freqs)
    # This band should represent time in radians.
    time = ee.Image(image).select('t')
    # Get the cosine terms.
    cosines = time.multiply(frequencies).cos().rename(cosNames)
    # Get the sin terms.
    sines = time.multiply(frequencies).sin().rename(sinNames)
    return image.addBands(cosines).addBands(sines)
  return addHarmonicsInner

# Function to get a sequence of band names for harmonic terms.
def constructBandNames(base, hlist):
  catname = [base + str(x) for x in hlist]
  return ee.List(catname)

#calculate predicted values from model coeffs
def predict_coeffs(independents,hTC):
  def predict_coeffsInner(image):
    return image.addBands(image.select(independents).multiply(hTC).reduce('sum').rename('fitted'))
  return predict_coeffsInner
#diff predicted and oberved, rescale by RMSE
def diff_predict(index):
  def diff_predictInner(image):
    return image.addBands(image.select(['fitted']).subtract(image.select([index])).rename('diff'))
  return diff_predictInner
