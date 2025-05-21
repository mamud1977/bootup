from pyspark import SparkContext
sc = SparkContext("local", "count app")
words = sc.parallelize (
   ["scala", 
   "java", 
   "hadoop", 
   "spark", 
   "akka",
   "spark vs hadoop", 
   "pyspark",
   "pyspark and spark"]
)
counts = words.count()
print ("============================================")
print (f"Number of elements in RDD -> {counts}")
print ("============================================")

coll = words.collect()
print ("============================================")
print (f"Elements in RDD -> {coll}")
print ("============================================")


print ("============================================")
def f(x): 
   print(x)
fore = words.foreach(f)
print ("============================================")


words_filter = words.filter(lambda x: 'spark' in x)
filtered = words_filter.collect()
print ("============================================")
print (f"Fitered RDD -> {filtered}")
print ("============================================")