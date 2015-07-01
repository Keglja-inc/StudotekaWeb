from studoteka import app

#---------------- POKRETANJE PROGRAMA --------------------
if __name__ == '__main__':
	#Server
    #app.run(host='0.0.0.0', port=8081)
    #app.run(host='0.0.0.0')
    #Localhost
    app.run(debug=True)