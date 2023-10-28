//SPDX-License-Identifier: GPL-3.0

pragma solidity >0.8.0;

contract FabricaContract{
    struct Producto {
        string nombre;
        uint id;
    }

    uint idDigits = 16; 
    Producto[] public productos;
    mapping (uint => address) public productoAPropietario;
    mapping (address => uint) public propietarioAProductos;

    
    event NuevoProducto(uint ArrayProdutid, string nombre, uint id);

    // Añadir producto
    function _crearProducto(string memory _nombre, uint _id) private {
         productos.push(Producto(_nombre, _id));
         emit  NuevoProducto(productos.length-1, _nombre, _id);
    }

    function _generarAlatorio(string memory _str) private view returns (uint){
        uint rand = uint(keccak256(abi.encodePacked(_str)));
        uint idModulus = 10 ^idDigits;
        return rand % idModulus;
    }

    function crearProductoAleatorio(string memory _nombre) public {
        uint randId = _generarAlatorio(_nombre);
        _crearProducto(_nombre, randId);
    }

    function propiedad(uint _productId) public {
        productoAPropietario[_productId] = msg.sender;
        propietarioAProductos[msg.sender]++;
    }

    function getProductosPorPropietario(address _propietario) external view returns (uint[] memory){
        uint contador = 0;
        uint[] memory resultado = new uint[](propietarioAProductos[_propietario]);

        for(uint i = 0; i<productos.length; i++){
            if (productoAPropietario[i] == _propietario) {
                resultado[contador] = productos[i].id;
                contador++;
            }
        }
        return resultado;
    }
}

