from pyspark import SparkContext

logFile = "file:///mnt/c/MyWork/Apache/logs/log.txt"  
sc = SparkContext("local", "first app")
logData = sc.textFile(logFile).cache()
numAs = logData.filter(lambda s: 'a' in s).count()
numBs = logData.filter(lambda s: 'b' in s).count()
print(f"Lines with a: {numAs}, lines with b: {numBs}")

