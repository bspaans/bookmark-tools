@echo off

set firstarg=%1

IF [%firstarg%]==[] (
	bm
) ELSE (
	set firstchar=%firstarg:~0,1%
	if [%firstchar%]==[-] (
		bm %firstarg%
	) ELSE (
		for /f %%X in ('bm %firstarg%') do cd %%X
	)
)

