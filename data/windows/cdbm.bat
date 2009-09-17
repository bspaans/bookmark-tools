@echo off

set firstarg=%1

IF [%firstarg%]==[] (
	bm
) ELSE (
	set firstchar=%firstarg:~0,1%
	if [%firstchar%]==[-] (
		bm %*
	) ELSE (
		for /f %%X in ('bm %*') do cd %%X
	)
)

