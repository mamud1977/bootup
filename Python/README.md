wsl
=======================================
Virtual Environment:
-----------------------

cd /mnt/c/MyWork/
python3 -m venv .venv
source .venv/bin/activate
deactivate

=======================================

cd 
cd /mnt/c/MyWork/gitlocal/bootup/Azure/
cd /mnt/c/MyWork/gitlocal/bootup/Python/
cd /mnt/c/MyWork/gitlocal/bootup/Python/Flask
cd /mnt/c/MyWork/gitlocal/bootup/Apache/PySpark

=======================================

pip list
pip install -r /mnt/c/MyWork/gitlocal/bootup/Python/requirements.txt
pip uninstall Flask
pip freeze > requirements.txt


---------------------------------
Steps to generate GitHub token:

1.Click your profile photo in the upper-right corner 
2. Select "Settings". 
3. Navigate to Developer settings: In the left sidebar, 
4. Click on "Developer settings". 
5. Click on "Personal access tokens". 
6. Generate a new token: Click on "Generate new token". 
7. Name the token
8. Set expiration
9. Select scopes
10. Generate the token: Click on "Generate token". 
11. Copy and secure the token

---------------------------------

GitHub Commands:

git clone --single-branch --branch branch1 https://github.com/mamud1977/bootup.git


