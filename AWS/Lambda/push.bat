@echo off
set filename=%~n1%~x1
set zip_filename=%1.zip
echo %zip_filename%

tar -acf %zip_filename% %1

aws s3 cp %zip_filename% s3://deployment-bucket-786x


