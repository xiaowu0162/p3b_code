# NAME: Di Wu,Jingnong Qu
# EMAIL: xiaowu200031@gmail.com,andrewqu2000@g.ucla.edu
# ID: 205117980,805126509
submission_files=lab3b.py Makefile README
default: lab3b
lab3b: lab3b.py
	ln -s $^ $@
	chmod u+x $@
dist: $(submission_files)
	tar -czvf lab3b-205117980.tar.gz $^
clean:
	rm -f lab3b *.tar.gz
