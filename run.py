from doc_anno_suite import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8000)
    # deployment command
    #app.run(host='0.0.0.0', debug=False, port=8000)