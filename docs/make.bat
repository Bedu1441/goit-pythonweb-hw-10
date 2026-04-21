@ECHO OFF

set SOURCEDIR=source
set BUILDDIR=build

sphinx-build -M html %SOURCEDIR% %BUILDDIR%