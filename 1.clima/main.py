from src import Clima


def main():
    clima = Clima("Asunción", "Paraguay")
    clima.actualizar_clima()
    clima.obtener_clima()
    print(clima)

    clima.cambiar_ciudad("Ciudad del Este", "Paraguay")
    clima.actualizar_clima()
    clima.obtener_clima()
    print(clima)

if __name__ == "__main__":
    main()
