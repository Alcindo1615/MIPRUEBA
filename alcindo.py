import os
import time
import json
import csv
import random
os.system('cls')

def cargarDatos():
    with open('tiendas.json', 'r', encoding='utf-8') as archivoTiendas:
        tiendas = json.load(archivoTiendas)
    with open('vendedores.json', 'r', encoding='utf-8') as archivoVendedores:
        vendedores = json.load(archivoVendedores)
    with open('ventas.json', 'r', encoding='utf-8') as asrchivoVentas:
        ventas = json.load(asrchivoVentas)
    return tiendas, vendedores, ventas


def guardarVenta(ventas):
    with open('ventas.json', 'w', encoding='utf-8') as archivoGuardar:
        json.dump(ventas, archivoGuardar, ensure_ascii=False, indent=4)

def crearCSV(estadisticas):
    with open('ESTADISTICA.csv', 'w', newline='\n', encoding='utf-8') as archivo:
        escribir = csv.writer(archivo)
        escribir.writerow(estadisticas)
        for estadistica in estadisticas:
            escribir.writerow([estadistica['venta_mayor'], estadistica['venta_minima'], estadistica['promedio_venta']])



def idVenta(ventas):
    id_venta = 0
    for venta in ventas['ventas']:
        if int(venta['id_venta']) > id_venta:
            id_venta = int(venta['id_venta'])
    return id_venta

def precarVenta(tiendas, vendedores, ventas):
    id_venta = idVenta(ventas)
    for i in range(500):
        id_venta += 1
        vendedor = random.choice(vendedores)
        id_vendedor = vendedor['id_vendedor']
        tienda = random.choice(tiendas)
        id_tienda = tienda['id_tienda']
        fecha = '04-07-2024'
        total_venta = random.choice(range(100_000, 300_000, 100))
        nuevaVenta = {
            'id_venta': id_venta,
            'id_vendedor': id_vendedor,
            'id_tienda': id_tienda,
            'fecha': fecha,
            'total_venta': total_venta
        }
        ventas['ventas'].append(nuevaVenta)
    print(ventas)
    print('Ventas precargadas con exito')
    display()



def crearVenta(vendedores, ventas):
    id_venta = idVenta(ventas)
    for vendedor in vendedores:
        print(f'ID: {vendedor["id_vendedor"]} -->> {vendedor["nombre"]} {vendedor["apellido"]}')
    print('---'*9)
    id_venta += 1
    id_vendedor = input('Ingrese el ID del empleado que realiza la venta: ')
    fecha = '04/07/2024'
    total_venta = int(input('Ingrese el monto de la venta: '))
    nuevaVenta = {
        "id_venta": id_venta,
        "id_vendedor": id_vendedor,
        "fecha": fecha,
        "total_venta": total_venta,
    }
    ventas['ventas'].append(nuevaVenta)
    guardarVenta(ventas)
    print('Venta Agregadas con exito')
    time.sleep(1)


def reporteSueldo(vendedores, ventas):
    for vendedor in vendedores:
        total_venta = 0
        bono = 0
        salud = int(vendedor['sueldo_base']*0.07)
        afp = int(vendedor['sueldo_base']*0.12)
        for venta in ventas['ventas']:
            if venta['id_vendedor'] == vendedor['id_vendedor']:
                total_venta = total_venta + venta['total_venta']
        if total_venta >= 5_000_000:
            bono = int(vendedor['sueldo_base']*0.15)
        elif total_venta >= 3_000_000:
            bono = int(vendedor['sueldo_base']*0.12)
        elif total_venta >= 1_000_000:
            bono = int(vendedor['sueldo_base']*0.1)
        sueldoLiquido = int(vendedor['sueldo_base']-salud-afp) + bono
        print(f'Nombre: {vendedor["nombre"]} {vendedor["apellido"]} | Sueldo Base: {vendedor["sueldo_base"]} | Bono: {bono} | Desc. Salud: {salud} | Desc. AFP: {afp} | Sueldo Liquido: {sueldoLiquido}')

def estadisticas(ventas):
    venta_mayor = max([venta['total_venta'] for venta in ventas['ventas']])
    venta_minima = min([venta['total_venta'] for venta in ventas['ventas']])
    total_venta = sum([venta['total_venta'] for venta in ventas['ventas']])
    promedio_venta = int(total_venta/len(ventas['ventas']))
    
    print(f'Venta mayor: {venta_mayor}')
    print(f'Venta minima: {venta_minima}')
    print(f'Promedio venta: {promedio_venta}')

    estadisticas = {
        'venta_mayor': venta_mayor,
        'venta_minima': venta_minima,
        'promedio_venta': promedio_venta
    }
    exportar = input('Desea exportar los datos a CSV ? (s/n): ')
    if exportar.lower() == 's':
        crearCSV(estadisticas)
        print('ARCHIVO EXPORTADO')
        display()
        limpiar()


def menuGeneral():
    print('-------- MENU GENERAL -------')
    print('[1] precargar ventas y guardar ventas.json')
    print('[2] crear nueva venta')
    print('[3] reporte de sueldo')
    print('[4] ver estadistica por tienda')
    print('[5] salir')

def limpiar():
    os.system('cls')

def display():
    time.sleep(1.5)

def errorLetra():
    print('*** La opción debe ser númerica ***')
    display()
    limpiar()

def errorRango():
    print('*** La opción esta fuera de rango ***')
    display()
    limpiar()

def main():
    tiendas, vendedores, ventas = cargarDatos()
    menu = True
    while menu:
        menuGeneral()
        opc1 = 0
        try:
            opc1 = int(input('\nIngrese una opción: '))
            if opc1 < 1 or opc1 > 5:
                errorRango()
            else:
                if opc1 == 1:
                    precarVenta(tiendas, vendedores, ventas)
                elif opc1 == 2:
                    crearVenta(vendedores, ventas)
                elif opc1 == 3:
                    reporteSueldo(vendedores, ventas)
                elif opc1 == 4:
                    estadisticas(ventas)  
                elif opc1 == 5:
                    limpiar()
                    print('<<< ¡Hasta Pronto! >>>')
                    display()
                    limpiar()
                    menu = False
        except:
            errorLetra()
if __name__ == '__main__':
    main()










