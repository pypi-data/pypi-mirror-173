import app

def test_add():
    app.is_test()
    #controllo se non esiste l'esame con la matricola "000"
    app.create()


def test_get_exam():
    app.is_test()
    app.get_exam("0")


def test_edit():
    app.is_test()
    app.edit("0")


def test_delete():
    app.is_test()
    #se esiste l'esame con la matricola "000" allora posso eliminarla
    app.delete("0")




