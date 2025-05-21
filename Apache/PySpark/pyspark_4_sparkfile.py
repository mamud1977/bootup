import os
from pyspark import SparkContext
from pyspark import SparkFiles

filepath = "/mnt/c/MyWork/Apache/sampledata"
filename = "AirPassengers.csv"

path = os.path.join(filepath, filename)

sc = SparkContext("local", "SparkFile App")
sc.addFile(path)

print (f"Root directory -> {SparkFiles.getRootDirectory()}")
print (f"Absolute Path -> {SparkFiles.get(path)}")



