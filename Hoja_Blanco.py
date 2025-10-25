import SASFU
aspirante1=SASFU.Aspirante("1312685560","Juan","Perez","JuaPere@gmail.com","090900933",True,9.02)
aspirante1.cargar_datos()
aspirante1.iniciar_sesion()
print(aspirante1.nacionalidad())
aspirante1.cerrar_sesion()
def test_nota_grado():
    assert aspirante1.nota_grado==9.02