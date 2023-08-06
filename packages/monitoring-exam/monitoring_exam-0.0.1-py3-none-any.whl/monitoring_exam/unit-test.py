import app

def test_check_voto():
    assert app.check_voto(21) == True


def test_limit_out_check_voto():
    assert  app.check_voto(31)  == False
    assert app.check_voto(17) == False


def test_limit_in_check_voto():
    assert app.check_voto(18) and app.check_voto(30)  == True


def test_negative_check_voto():
    assert app.check_voto(-19)  == False
