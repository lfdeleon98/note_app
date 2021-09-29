from website import create_app

app = create_app()

#this says only if we run this file are we going to execute the next line
#if we import another main.py from another file, it can run the webserver, and we dont want that
if __name__ == '__main__':
    #anytime we make a change to our python code, it will automatically rerun the webserver (turn it off during production)
    app.run(debug=True)