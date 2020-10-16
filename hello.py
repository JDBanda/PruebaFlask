'''
Elaboró: Javier David Banda Villeda
Para usar Flask importelo, jsonify convierte el texto plano en un JSON
'''
from flask import Flask, jsonify, request
app = Flask(__name__) #Esta cosa inicia la aplicación

#Importar productos
from products import products

@app.route('/') #Ruta del inicio
def hello_world(): #Devuelve la cadena en pantalla
    return 'Hola Mundo!'

@app.route('/jsoneado') #Ruta con un textoen JSON
def getJson():
    return jsonify({"message":"MODO JSON!"})

@app.route('/products') #muestra la lista de productos del archivo products.py
def getProducts():
    return jsonify({"products": products, "message": "OK!"}) #si ponemos solo products, igual jala pero no tiene buen formato

'''
Este método trata de emular un filtrado de busqueda por ruta
en el navegador se debe introducir el nombre del producto después
de "products/"
'''
@app.route('/products/<string:product_name>') #<string:product_name> significa que hay un parámetro de tipo string
def getProduct(product_name):
    #1. Se recorre el arreglo (JSON) de productos, es verdadero si el nombre del parámetro coincide con el del arreglo 
    productsFound = [product for product in products if product['name'] == product_name]
    #2. Validar que haya productos si la longitud de productsFound es mayor a 0
    if (len(productsFound) > 0):
        #2.a) Devuelve si esta
        return jsonify({"product": productsFound[0]})
    #2.b) Devuelve un mensaje si no esta
    return jsonify({"message": "Producto no encontrado"})

#Metodo POST para guardar datos, obvio que aquí es temporal, no importa si es la misma ruta
# debido a que cambia la firma del método se puede repetir la ruta que recibe ciertos parámetros
@app.route('/products', methods=['POST']) #es methods no method, si no no funciona el request
#Método para crear nuevos productos
def createProduct():
    #new_producto es un objeto que contiene los elementos JSON de la solicitud POST
    '''
    OJO VIEJO, ASI SE CREAN LOS ENDPOINTS
    '''
    new_product = {
        "name": request.args['name'],
        "price": request.args['price'],
        "quantity": request.args['quantity']
    }
    #Aqui se guardan pues
    products.append(new_product)
    return jsonify({"message": "Success!", "products":products})

#Método PUT para editar datos, edita a través del nombre
@app.route('/products/<string:product_name>', methods=['PUT'])
#Se le pasa el parámetro del nombre
def editProduct(product_name):
    #Igual que antes se verifica si existe
    productFound = [product for product in products if product['name'] == product_name]
    if (len(productFound) > 0):
        #Se pasan los valores del request a los del product found
        productFound[0]['name'] = request.json['name']
        productFound[0]['price'] = request.json['price']
        productFound[0]['quantity'] = request.json['quantity']
        #Se imprime
        return jsonify({
            "message": "Product updated",
            "product": productFound[0]
        })
    #No existe algo que editar
    return jsonify({"message": "Product not found"})

#Método DELETE para borrar datos, elimina a través del nombre, es muy similar al anterior
#solo cambia la instrucción interna
@app.route('/products/<string:product_name>', methods=['DELETE'])
#Se le pasa el parámetro del nombre
def deleteProduct(product_name):
    #Igual que antes se verifica si existe
    productFound = [product for product in products if product['name'] == product_name]
    if (len(productFound) > 0):
        #Se elimina
        products.remove(productFound[0])
        #Se imprime
        return jsonify({
            "message": "Product deleted",
            "product": products
        })
    #No existe algo que editar
    return jsonify({"message": "Product not found"})

#Esto siempre debe ir hasta abajo si no vale kk, son como configuraciones generales
if __name__ == '__main__':
    app.run(debug=True)