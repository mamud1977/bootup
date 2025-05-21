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

words_map = words.map(lambda x: (x, 1))
mapping = words_map.collect()
print ("============================================")
print (f"Key value pair -> {mapping}")
print ("============================================")

nums = sc.parallelize([1, 2, 3, 4, 5])
adding = nums.reduce(add)
print (f"Adding all the elements -> {adding}")

