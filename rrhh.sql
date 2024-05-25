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

CREATE TABLE `Trabajador` (
  `run_trabajador` varchar(255) PRIMARY KEY,
  `nombre` varchar(255),
  `correo` varchar(255),
  `cargo` varchar(255),
  `sueldo` integer,
  `fecha_ingreso` date,
  `id_departamento` integer
);

ALTER TABLE `Sucursal_Departamento` ADD FOREIGN KEY (`id_sucursal`) REFERENCES `Sucursal` (`id_sucursal`);

ALTER TABLE `Sucursal_Departamento` ADD FOREIGN KEY (`id_departamento`) REFERENCES `Departamento` (`id_departamento`);

ALTER TABLE `Trabajador` ADD FOREIGN KEY (`id_departamento`) REFERENCES `Departamento` (`id_departamento`);
