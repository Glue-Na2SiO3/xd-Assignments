###############################################################################
# Makefile for project 
###############################################################################

## General options
PROJECT = 
MCU = 8086
COMPILER = "MASM32"
TARGET = Debug
SHELL = C:\Windows\system32\cmd.exe

## Tools general options
ASMFLAGS=/c /Zd /Zi
LDFLAGS=/CODEVIEW

## Processing Tools
ASM=ml.exe
LD=link16.exe
#  D:/Desktop/微机原理实验/微机第五次实验/8086_1/Debug/Debug.exe: TOOL=LD
#     D:/Desktop/微机原理实验/微机第五次实验/8086_1/Debug/qwe.obj: TOOL=ASM
#        D:/Desktop/微机原理实验/微机第五次实验/qwe.asm

# Build tree:
all:	Debug

Debug:	Debug.exe

Debug.exe:	qwe.obj 
	$(LD) $(LDFLAGS) qwe.obj,Debug.exe,nul.map,,,

qwe.obj:	../../qwe.asm 
	$(ASM) $(ASMFLAGS) ../../qwe.asm

# tidy - delete all temporary files which are not involved in the target generation
tidy:

# cleanup - delete all generated files
clean:	tidy
	rm -rf Debug.exe
	rm -rf qwe.obj
