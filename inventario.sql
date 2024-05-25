CREATE TABLE `Producto` (
  `id_producto` integer PRIMARY KEY AUTO_INCREMENT,
  `nombre` varchar(255),
  `precio_venta` integer,
  `precio_compra` integer,
  `categoria` varchar(255)
);

CREATE TABLE `Stock_Sucursal` (
  `stock_id` integer PRIMARY KEY AUTO_INCREMENT,
  `stock` integer,
  `producto_id` integer,
  `sucursal_id` integer
);

CREATE TABLE `Sucursal` (
  `id_sucursal` integer PRIMARY KEY AUTO_INCREMENT,
  `direccion` varchar(255),
  `nombre` varchar(255)
);

CREATE TABLE `Departamento` (
  `id_departamento` integer PRIMARY KEY AUTO_INCREMENT,
  `nombre` varchar(255)
);

CREATE TABLE `Sucursal_Departamento` (
  `id_sucursal_departamento` integer PRIMARY KEY AUTO_INCREMENT,
  `id_sucursal` integer,
  `id_departamento` integer
);

ALTER TABLE `Stock_Sucursal` ADD FOREIGN KEY (`producto_id`) REFERENCES `Producto` (`id_producto`);

ALTER TABLE `Stock_Sucursal` ADD FOREIGN KEY (`sucursal_id`) REFERENCES `Sucursal` (`id_sucursal`);

ALTER TABLE `Sucursal_Departamento` ADD FOREIGN KEY (`id_sucursal`) REFERENCES `Sucursal` (`id_sucursal`);

ALTER TABLE `Sucursal_Departamento` ADD FOREIGN KEY (`id_departamento`) REFERENCES `Departamento` (`id_departamento`);
