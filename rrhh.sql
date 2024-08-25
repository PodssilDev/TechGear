-- Base de Datos MySQL
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

-- Crear la tabla Trabajador
-- Descripcion: Tabla que almacena los trabajadores de la empresa
CREATE TABLE `Trabajador` (
  `run_trabajador` VARBINARY(255) PRIMARY KEY,  -- Llave primaria, identificador único del trabajador (encriptado)
  `nombre` VARCHAR(255),  -- Nombre del trabajador
  `correo` VARCHAR(255),  -- Correo electrónico del trabajador
  `cargo` VARCHAR(255),  -- Cargo del trabajador
  `sueldo` VARBINARY(255),  -- Sueldo del trabajador (encriptado)
  `fecha_ingreso` DATE,  -- Fecha de ingreso del trabajador
  `id_departamento` INTEGER,  -- Identificador del departamento al que pertenece el trabajador
  FOREIGN KEY (`id_departamento`) REFERENCES `Departamento` (`id_departamento`)
);

-- Añadir llave foránea en la tabla Sucursal_Departamento para asociarla con la tabla Sucursal
ALTER TABLE `Sucursal_Departamento` ADD FOREIGN KEY (`id_sucursal`) REFERENCES `Sucursal` (`id_sucursal`);

-- Añadir llave foránea en la tabla Sucursal_Departamento para asociarla con la tabla Departamento
ALTER TABLE `Sucursal_Departamento` ADD FOREIGN KEY (`id_departamento`) REFERENCES `Departamento` (`id_departamento`);

-- Añadir llave foránea en la tabla Trabajador para asociarla con la tabla Departamento
ALTER TABLE `Trabajador` ADD FOREIGN KEY (`id_departamento`) REFERENCES `Departamento` (`id_departamento`);