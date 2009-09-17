@echo off

set command=%1 



if %command:~0,1% == "-" do bm 

for /f %%X in ('bm %i') do cd %%X

