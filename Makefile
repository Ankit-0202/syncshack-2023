all:
	npm run dev

install:
	pip3 install -r requirements.txt

a:
	git add -A
	git commit -m 'Ankit made changes'
	git push

c:
	git add -A
	git commit -m 'Chris made changes'
	git push

t:
	git add -A
	git commit -m 'Tim made changes'
	git push

d:
	git add -A
	git commit -m 'Daniel made changes'
	git push