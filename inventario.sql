-- Base de Datos MySQL
-- Crear la tabla Producto
-- Descripcion: Tabla que almacena los productos disponibles en el inventario
CREATE TABLE `Producto` (
  `id_producto` integer PRIMARY KEY AUTO_INCREMENT,  -- Llave primaria, identificador único del producto, generado automáticamente
  `nombre` varchar(255),  -- Nombre del producto
  `precio_venta` integer,  -- Precio de venta del producto
  `precio_compra` integer,  -- Precio de compra del producto
  `categoria` varchar(255)  -- Categoría del producto
);

-- Crear la tabla Stock_Sucursal
-- Descripcion: Tabla que almacena el stock de productos en cada sucursal
CREATE TABLE `Stock_Sucursal` (
  `stock_id` integer PRIMARY KEY AUTO_INCREMENT,  -- Llave primaria, identificador único del stock, generado automáticamente
  `stock` integer,  -- Cantidad de stock
  `producto_id` integer,  -- Identificador del producto asociado
  `sucursal_id` integer  -- Identificador de la sucursal asociada
);

-- Crear la tabla Sucursal
-- Descripcion: Tabla que almacena las sucursales de la empresa
CREATE TABLE `Sucursal` (
  `id_sucursal` integer PRIMARY KEY AUTO_INCREMENT,  -- Llave primaria, identificador único de la sucursal, generado automáticamente
  `direccion` varchar(255),  -- Dirección de la sucursal
  `nombre` varchar(255)  -- Nombre de la sucursal
);

-- Crear la tabla Departamento
-- Descripcion: Tabla que almacena los departamentos de la empresa
CREATE TABLE `Departamento` (
  `id_departamento` integer PRIMARY KEY AUTO_INCREMENT,  -- Llave primaria, identificador único del departamento, generado automáticamente
  `nombre` varchar(255)  -- Nombre del departamento
);

-- Crear la tabla Sucursal_Departamento
-- Descripcion: Tabla que almacena la relación entre sucursales y departamentos
CREATE TABLE `Sucursal_Departamento` (
  `id_sucursal_departamento` integer PRIMARY KEY AUTO_INCREMENT,  -- Llave primaria, identificador único de la relación sucursal-departamento, generado automáticamente
  `id_sucursal` integer,  -- Identificador de la sucursal asociada
  `id_departamento` integer  -- Identificador del departamento asociado
);

-- Añadir llave foránea en la tabla Stock_Sucursal para asociarla con la tabla Producto
ALTER TABLE `Stock_Sucursal` ADD FOREIGN KEY (`producto_id`) REFERENCES `Producto` (`id_producto`);

-- Añadir llave foránea en la tabla Stock_Sucursal para asociarla con la tabla Sucursal
ALTER TABLE `Stock_Sucursal` ADD FOREIGN KEY (`sucursal_id`) REFERENCES `Sucursal` (`id_sucursal`);

-- Añadir llave foránea en la tabla Sucursal_Departamento para asociarla con la tabla Sucursal
ALTER TABLE `Sucursal_Departamento` ADD FOREIGN KEY (`id_sucursal`) REFERENCES `Sucursal` (`id_sucursal`);

-- Añadir llave foránea en la tabla Sucursal_Departamento para asociarla con la tabla Departamento
ALTER TABLE `Sucursal_Departamento` ADD FOREIGN KEY (`id_departamento`) REFERENCES `Departamento` (`id_departamento`);