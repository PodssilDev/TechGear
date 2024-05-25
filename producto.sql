CREATE TABLE [Producto] (
  [id_producto] integer PRIMARY KEY IDENTITY(1, 1),
  [nombre] nvarchar(255),
  [precio_venta] integer,
  [precio_compra] integer,
  [categoria] nvarchar(255),
  [rut_proveedor] nvarchar(255)
)
GO

CREATE TABLE [Proveedor] (
  [rut_proveedor] nvarchar(255) PRIMARY KEY,
  [nombre] nvarchar(255),
  [direccion] nvarchar(255)
)
GO

CREATE TABLE [Stock_Sucursal] (
  [stock_id] integer PRIMARY KEY IDENTITY(1, 1),
  [stock] integer,
  [producto_id] integer,
  [sucursal_id] integer
)
GO

CREATE TABLE [Sucursal] (
  [id_sucursal] integer PRIMARY KEY IDENTITY(1, 1),
  [direccion] nvarchar(255),
  [nombre] nvarchar(255)
)
GO

ALTER TABLE [Stock_Sucursal] ADD FOREIGN KEY ([producto_id]) REFERENCES [Producto] ([id_producto])
GO

ALTER TABLE [Stock_Sucursal] ADD FOREIGN KEY ([sucursal_id]) REFERENCES [Sucursal] ([id_sucursal])
GO

ALTER TABLE [Producto] ADD FOREIGN KEY ([rut_proveedor]) REFERENCES [Proveedor] ([rut_proveedor])
GO
