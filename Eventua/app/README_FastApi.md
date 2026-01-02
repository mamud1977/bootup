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
uvicorn app.main:app --reload





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
