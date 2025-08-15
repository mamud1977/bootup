
import os 
  
# Get the value of 'HOME' 
key = 'HOME'
value = os.getenv(key) 
print(f"{key} : {value}")  

# Get the value of 'HOME' 
key = 'API_KEY'
value = os.getenv('API_KEY') 
print(f"{key} : {value}")  
  
