frontend:
	npm run dev

backend:
	flask --app app run --debug

install:
	pip3 install -r requirements.txt
	npm install

clean:
	rm -f output.json
	rm -rf __pycache__





###############
##### GIT #####
###############

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