.PHONY: clean all

all:
	#uglifyjs js/* main.js -o bundle.js -c
	lessc less/* bundle.css

clean:
	rm -f bundle.*

install:
	npm install -g uglify-js
	npm install -g less
