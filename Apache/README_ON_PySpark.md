Instalation:-----------
Start WSL and go to desired folder

sudo apt update
sudo apt install openjdk-17-jdk  # for Java 17 
java --version

https://www.tutorialspoint.com/pyspark/pyspark_environment_setup.htm

Download:
    spark-3.5.5-bin-hadoop3.tgz
Extract:
    tar -xvf spark-3.5.5-bin-hadoop3.tgz

Environment Varibales:
    export SPARK_HOME=/mnt/c/MyWork/Apache/spark-3.5.5-bin-hadoop3
    export PATH=$PATH:/mnt/c/MyWork/Apache/spark-3.5.5-bin-hadoop3
    export PYTHONPATH=$SPARK_HOME/python:$SPARK_HOME/python/lib/py4j-0.10.4-src.zip:$PYTHONPATH
    export PATH=$SPARK_HOME/python:$PATH

Save the above envt variables in .bashrc

Run "source .bashrc"

Go to Spark directory and invoke PySpark shell:
    ./bin/pyspark

To execute a PySpark code:
    $SPARK_HOME/bin/spark-submit pyspark_4_sparkfile.py




