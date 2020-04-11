// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.
(LOOP)
	@KBD
	D=M // D=R[KBD]
	@BLACK
	D;JGT // If D >0 goto BLACK
	(WHITE)
		@i // i refers to some mem. location.
		M=0 // i=0
		(WHITELOOP)
			@i
			D=M // D=i
			@8191
			D=D-A // D=i-100
			@WHITEEND
			D;JGT // If (i-8191)>0 goto WHITEEND

			@SCREEN
			D=A //D=SCREEN
			@i
			A=D+M // address=SCREEN+i
			M=0
			@i
			M=M+1 // i=i+1

			@WHITELOOP
			0;JMP // Goto LOOP
	(WHITEEND)
	@LOOP
	0;JMP


	(BLACK)
		@i // i refers to some mem. location.
		M=0 // i=0
		(BLACKLOOP)
			@i
			D=M // D=i
			@8191
			D=D-A // D=i-100
			@BLACKEND
			D;JGT // If (i-8191)>0 goto BLACKEND

			@SCREEN
			D=A
			@i
			A=D+M // address=SCREEN+i
			M=-1
			@i
			M=M+1 // i=i+1
			@BLACKLOOP
			0;JMP // Goto LOOP
	(BLACKEND)
	@LOOP
	0;JMP // Goto LOOP