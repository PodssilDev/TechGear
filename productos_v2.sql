-- Base de Datos SQL Server
-- Eliminar la tabla Stock_Sucursal si existe
DROP TABLE IF EXISTS Stock_Sucursal;

-- Eliminar la tabla Producto si existe
DROP TABLE IF EXISTS Producto;

-- Eliminar la tabla Sucursal si existe
DROP TABLE IF EXISTS Sucursal;

-- Eliminar la tabla Sucursal si existe
DROP TABLE IF EXISTS Proveedor;

-- Crear la tabla Proveedor
-- Descripcion: Tabla que almacena los proveedores de la tienda
CREATE TABLE Proveedor (
    rut_proveedor VARCHAR(20) PRIMARY KEY,  -- Clave primaria, identificador único del proveedor
    nombre VARCHAR(255) NOT NULL,  -- Nombre del proveedor, no puede ser nulo
    direccion VARCHAR(255)  -- Dirección del proveedor
);

-- Crear la tabla Producto
-- Descripcion: Tabla que almacena los productos disponibles en la tienda
CREATE TABLE Producto (
    id_producto INT PRIMARY KEY,  -- Clave primaria, identificador único del producto
    nombre VARCHAR(255) NOT NULL,  -- Nombre del producto, no puede ser nulo
    precio_venta INT NOT NULL,  -- Precio de venta del producto, no puede ser nulo
    precio_compra INT NOT NULL,  -- Precio de compra del producto, no puede ser nulo
    categoria VARCHAR(255),  -- Categoría del producto
    rut_proveedor VARCHAR(20),  -- Identificador del proveedor asociado al producto
    FOREIGN KEY (rut_proveedor) REFERENCES Proveedor(rut_proveedor)  -- Clave foránea que referencia a la tabla Proveedor
);

-- Crear la tabla Sucursal
-- Descripcion: Tabla que almacena las sucursales de la tienda
CREATE TABLE Sucursal (
    id_sucursal INT PRIMARY KEY,  -- Clave primaria, identificador único de la sucursal
    direccion VARCHAR(255),  -- Dirección de la sucursal
    nombre VARCHAR(255) NOT NULL  -- Nombre de la sucursal, no puede ser nulo
);

-- Crear la tabla Stock_Sucursal
-- Descripcion: Tabla que almacena el stock de productos en cada sucursal
CREATE TABLE Stock_Sucursal (
    stock_id INT PRIMARY KEY,  -- Clave primaria, identificador único del stock
    stock INT NOT NULL,  -- Cantidad de stock, no puede ser nulo
    producto_id INT,  -- Identificador del producto asociado
    sucursal_id INT,  -- Identificador de la sucursal asociada
    FOREIGN KEY (producto_id) REFERENCES Producto(id_producto),  -- Clave foránea que referencia a la tabla Producto
    FOREIGN KEY (sucursal_id) REFERENCES Sucursal(id_sucursal)  -- Clave foránea que referencia a la tabla Sucursal
);