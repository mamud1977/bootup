###### env setup for Windows

find . -name "__pycache__" -type d -exec rm -r {} +

wsl
cd /mnt/c/MyWork/gitlocal/bootup/FastApi
source .venv/bin/activate
export PYTHONPYCACHEPREFIX=/mnt/c/MyWork/gitlocal/bootup/FastApi/pycache

deactivate

# In Windows

cd C:\MyWork\gitlocal\bootup\Eventua
python -m venv .venv
.\.venv\Scripts\activate.bat
set STORAGE_TYPE=cloud
set UPLOAD_FOLDER=eventua_local_bucket
set AWS_S3_BUCKET=eventua-s3-bucket2
set AWS_REGION=us-east-1
set AWS_ACCESS_KEY_ID=xxx
set AWS_SECRET_ACCESS_KEY=xxx
uvicorn app.main:app --reload --port 8000



# Cloud storage config
S3_BUCKET = os.getenv("S3_BUCKET", "eventua_s3_bucket")

echo %STORAGE_TYPE%
echo %S3_BUCKET%
echo %AWS_REGION%
echo %AWS_ACCESS_KEY_ID%
echo %AWS_SECRET_ACCESS_KEY%



###### pip 

pip install -r app\requirements.txt

###### uvicorn

uvicorn main_with_db:app --reload
uvicorn main:app --reload

uvicorn main:app --reload --reload-delay 1

uvicorn main:app --reload --host 127.0.0.1 --port 8000

uvicorn main:app --reload --reload-dir templates --host 127.0.0.1 --port 8000

uvicorn main:app \
    --reload \
    --reload-dir /mnt/c/MyWork/gitlocal/bootup/FastApi/routers

uvicorn main:app \
  --reload \
  --reload-dir /mnt/c/MyWork/gitlocal/bootup/FastApi




###### openssl

$ openssl rand -hex 32
0f393ba18b31bdc9e83a3538fa4b68ef5725345d398d1cacf7365f42748a83d3


###### Temporary Public Tunnel
  1) Install ngrok
  2) Go to https://dashboard.ngrok.com/endpoints
  3) Get AuthToken
  4) Get Domain
  5) Run below command:

    ngrok http --domain=ahmed-pachydermoid-autogenously.ngrok-free.dev 8000
  6) Test using below:
    https://ahmed-pachydermoid-autogenously.ngrok-free.dev/



