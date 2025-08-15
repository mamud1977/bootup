from pydantic import HttpUrl, Field
from pydantic_settings import BaseSettings

class AppConfig(BaseSettings):
    DATABASE_HOST: HttpUrl
    DATABASE_USER: str = Field(min_length=2)
    DATABASE_PASSWORD: str = Field(min_length=10)
    API_KEY: str = Field(min_length=20)

# From command prompt, set below environment variables 
# $ export DATABASE_HOST='https://lriigsp-oo89314.snowflakecomputing.com/console/login'
# $ export DATABASE_USER='Test_User'
# $ export DATABASE_PASSWORD='Test_Password'
# $ export API_KEY='API_KEYbyMamud0923kjds89kklslsl%%%92##kkdCCCCest'


a = AppConfig() 

print(a)