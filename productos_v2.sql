DROP TABLE IF EXISTS Stock_Sucursal;
DROP TABLE IF EXISTS Producto;
DROP TABLE IF EXISTS Sucursal;
DROP TABLE IF EXISTS Proveedor;

CREATE TABLE Proveedor (
    rut_proveedor VARCHAR(20) PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    direccion VARCHAR(255)
);

CREATE TABLE Producto (
    id_producto INT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    precio_venta INT NOT NULL,
    precio_compra INT NOT NULL,
    categoria VARCHAR(255),
    rut_proveedor VARCHAR(20),
    FOREIGN KEY (rut_proveedor) REFERENCES Proveedor(rut_proveedor)
);

CREATE TABLE Sucursal (
    id_sucursal INT PRIMARY KEY,
    direccion VARCHAR(255),
    nombre VARCHAR(255) NOT NULL
);

CREATE TABLE Stock_Sucursal (
    stock_id INT PRIMARY KEY,
    stock INT NOT NULL,
    producto_id INT,
    sucursal_id INT,
    FOREIGN KEY (producto_id) REFERENCES Producto(id_producto),
    FOREIGN KEY (sucursal_id) REFERENCES Sucursal(id_sucursal)
);
