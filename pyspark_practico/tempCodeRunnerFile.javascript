import fs from 'fs';

let fields = {
    "fields": [
        {
            "metadata": {},
            "name": "_hoodie_commit_time",
            "nullable": true,
            "type": "string"
        },
        {
            "metadata": {},
            "name": "_hoodie_commit_seqno",
            "nullable": true,
            "type": "string"
        },
        {
            "metadata": {},
            "name": "_hoodie_record_key",
            "nullable": true,
            "type": "string"
        },
        {
            "metadata": {},
            "name": "_hoodie_partition_path",
            "nullable": true,
            "type": "string"
        },
        {
            "metadata": {},
            "name": "_hoodie_file_name",
            "nullable": true,
            "type": "string"
        },
        {
            "metadata": {},
            "name": "IDDMS",
            "nullable": true,
            "type": "string"
        },
        {
            "metadata": {},
            "name": "IDDealer",
            "nullable": true,
            "type": "string"
        },
        {
            "metadata": {},
            "name": "GUID",
            "nullable": true,
            "type": "string"
        },
        {
            "metadata": {},
            "name": "FechaExtraccion",
            "nullable": true,
            "type": "string"
        },
        {
            "metadata": {},
            "name": "FechaFactura",
            "nullable": true,
            "type": "string"
        },
        {
            "metadata": {},
            "name": "FechaApertura",
            "nullable": true,
            "type": "string"
        },
        {
            "metadata": {},
            "name": "HoraApertura",
            "nullable": true,
            "type": "string"
        },
        {
            "metadata": {},
            "name": "FechaRecepcion",
            "nullable": true,
            "type": "string"
        },
        {
            "metadata": {},
            "name": "HoraRecepcion",
            "nullable": true,
            "type": "string"
        },
        {
            "metadata": {},
            "name": "FechaEntrega",
            "nullable": true,
            "type": "string"
        },
        {
            "metadata": {},
            "name": "Hora",
            "nullable": true,
            "type": "string"
        },
        {
            "metadata": {},
            "name": "FechaCierre",
            "nullable": true,
            "type": "string"
        },
        {
            "metadata": {},
            "name": "Hora1",
            "nullable": true,
            "type": "string"
        },
        {
            "metadata": {},
            "name": "Factura",
            "nullable": true,
            "type": "string"
        },
        {
            "metadata": {},
            "name": "Taller",
            "nullable": true,
            "type": "string"
        },
        {
            "metadata": {},
            "name": "TipoOrden",
            "nullable": true,
            "type": "string"
        },
        {
            "metadata": {},
            "name": "TipoPago",
            "nullable": true,
            "type": "string"
        },
        {
            "metadata": {},
            "name": "NumeroOT",
            "nullable": true,
            "type": "string"
        },
        {
            "metadata": {},
            "name": "CodigoOperacion",
            "nullable": true,
            "type": "string"
        },
        {
            "metadata": {},
            "name": "Descripcion",
            "nullable": true,
            "type": "string"
        },
        {
            "metadata": {},
            "name": "NumeroParte",
            "nullable": true,
            "type": "string"
        },
        {
            "metadata": {},
            "name": "Venta",
            "nullable": true,
            "type": "string"
        },
        {
            "metadata": {},
            "name": "Descuento",
            "nullable": true,
            "type": "string"
        },
        {
            "metadata": {},
            "name": "Costo",
            "nullable": true,
            "type": "string"
        },
        {
            "metadata": {},
            "name": "Tipo",
            "nullable": true,
            "type": "string"
        },
        {
            "metadata": {},
            "name": "HorasPagadas",
            "nullable": true,
            "type": "string"
        },
        {
            "metadata": {},
            "name": "HorasFacturadas",
            "nullable": true,
            "type": "string"
        },
        {
            "metadata": {},
            "name": "NumeroAsesor",
            "nullable": true,
            "type": "string"
        },
        {
            "metadata": {},
            "name": "NombreAsesor",
            "nullable": true,
            "type": "string"
        },
        {
            "metadata": {},
            "name": "RFC",
            "nullable": true,
            "type": "string"
        },
        {
            "metadata": {},
            "name": "NombreCliente",
            "nullable": true,
            "type": "string"
        },
        {
            "metadata": {},
            "name": "Direccion",
            "nullable": true,
            "type": "string"
        },
        {
            "metadata": {},
            "name": "Telefonos",
            "nullable": true,
            "type": "string"
        },
        {
            "metadata": {},
            "name": "CP",
            "nullable": true,
            "type": "string"
        },
        {
            "metadata": {},
            "name": "Email",
            "nullable": true,
            "type": "string"
        },
        {
            "metadata": {},
            "name": "NombreAseguradora",
            "nullable": true,
            "type": "string"
        },
        {
            "metadata": {},
            "name": "ClaveSiniestro",
            "nullable": true,
            "type": "string"
        },
        {
            "metadata": {},
            "name": "NombreFlotilla",
            "nullable": true,
            "type": "string"
        },
        {
            "metadata": {},
            "name": "Odometro",
            "nullable": true,
            "type": "string"
        },
        {
            "metadata": {},
            "name": "VIN",
            "nullable": true,
            "type": "string"
        },
        {
            "metadata": {},
            "name": "Anio",
            "nullable": true,
            "type": "string"
        },
        {
            "metadata": {},
            "name": "FechaEntrega1",
            "nullable": true,
            "type": "string"
        },
        {
            "metadata": {},
            "name": "Marca",
            "nullable": true,
            "type": "string"
        },
        {
            "metadata": {},
            "name": "Modelo",
            "nullable": true,
            "type": "string"
        },
        {
            "metadata": {},
            "name": "Color",
            "nullable": true,
            "type": "string"
        },
        {
            "metadata": {},
            "name": "Interior",
            "nullable": true,
            "type": "string"
        },
        {
            "metadata": {},
            "name": "TipoServicio",
            "nullable": true,
            "type": "string"
        },
        {
            "metadata": {},
            "name": "ClaveComercial",
            "nullable": true,
            "type": "string"
        },
        {
            "metadata": {},
            "name": "TipoPaquetesAccesorios",
            "nullable": true,
            "type": "string"
        },
        {
            "metadata": {},
            "name": "TipoPaquetesRefaccioness",
            "nullable": true,
            "type": "string"
        },
        {
            "metadata": {},
            "name": "StatusOR",
            "nullable": true,
            "type": "string"
        },
        {
            "metadata": {},
            "name": "SubTipoOrden",
            "nullable": true,
            "type": "string"
        },
        {
            "metadata": {},
            "name": "CategoriaMecanico",
            "nullable": true,
            "type": "string"
        },
        {
            "metadata": {},
            "name": "FechaPromesa",
            "nullable": true,
            "type": "string"
        },
        {
            "metadata": {},
            "name": "ID_TipoServicio",
            "nullable": true,
            "type": "string"
        },
        {
            "metadata": {},
            "name": "SuperOrden",
            "nullable": true,
            "type": "string"
        },
        {
            "metadata": {},
            "name": "idGUID",
            "nullable": true,
            "type": "string"
        },
        {
            "metadata": {},
            "name": "idClienteSF",
            "nullable": true,
            "type": "string"
        },
        {
            "metadata": {},
            "name": "idClienteDMS",
            "nullable": true,
            "type": "string"
        },
        {
            "metadata": {},
            "name": "tipoPersona",
            "nullable": true,
            "type": "string"
        },
        {
            "metadata": {},
            "name": "cargoNombramiento",
            "nullable": true,
            "type": "string"
        },
        {
            "metadata": {},
            "name": "nombre",
            "nullable": true,
            "type": "string"
        },
        {
            "metadata": {},
            "name": "apellidoPaterno",
            "nullable": true,
            "type": "string"
        },
        {
            "metadata": {},
            "name": "apellidoMaterno",
            "nullable": true,
            "type": "string"
        },
        {
            "metadata": {},
            "name": "razonSocial",
            "nullable": true,
            "type": "string"
        },
        {
            "metadata": {},
            "name": "telefono_cliente",
            "nullable": true,
            "type": "string"
        },
        {
            "metadata": {},
            "name": "telefono2",
            "nullable": true,
            "type": "string"
        },
        {
            "metadata": {},
            "name": "numeroCelular",
            "nullable": true,
            "type": "string"
        },
        {
            "metadata": {},
            "name": "TelefonoOficina",
            "nullable": true,
            "type": "string"
        },
        {
            "metadata": {},
            "name": "extTelefonoOficina",
            "nullable": true,
            "type": "string"
        },
        {
            "metadata": {},
            "name": "telefonoAsistente",
            "nullable": true,
            "type": "string"
        },
        {
            "metadata": {},
            "name": "correo",
            "nullable": true,
            "type": "string"
        },
        {
            "metadata": {},
            "name": "sexo",
            "nullable": true,
            "type": "string"
        },
        {
            "metadata": {},
            "name": "rfc_cliente",
            "nullable": true,
            "type": "string"
        },
        {
            "metadata": {},
            "name": "fechaNacimiento",
            "nullable": true,
            "type": "string"
        },
        {
            "metadata": {},
            "name": "Nombre_contactoPersonaMoral",
            "nullable": true,
            "type": "string"
        },
        {
            "metadata": {},
            "name": "apellidoPaterno_contactoPersonaMoral",
            "nullable": true,
            "type": "string"
        },
        {
            "metadata": {},
            "name": "ApellidoMaterno_contactoPersonaMoral",
            "nullable": true,
            "type": "string"
        },
        {
            "metadata": {},
            "name": "telefono_contactoPersonaMoral",
            "nullable": true,
            "type": "string"
        },
        {
            "metadata": {},
            "name": "numeroCelular_contactoPersonaMoral",
            "nullable": true,
            "type": "string"
        },
        {
            "metadata": {},
            "name": "TelefonoOficina_contactoPersonaMoral",
            "nullable": true,
            "type": "string"
        },
        {
            "metadata": {},
            "name": "extTelefonoOficina_contactoPersonaMoral",
            "nullable": true,
            "type": "string"
        },
        {
            "metadata": {},
            "name": "telefonoAsistente_contactoPersonaMoral",
            "nullable": true,
            "type": "string"
        },
        {
            "metadata": {},
            "name": "correo_contactoPersonaMoral",
            "nullable": true,
            "type": "string"
        },
        {
            "metadata": {},
            "name": "_uuid",
            "nullable": true,
            "type": "string"
        },
        {
            "metadata": {},
            "name": "_source_file",
            "nullable": true,
            "type": "string"
        },
        {
            "metadata": {},
            "name": "_export_date",
            "nullable": true,
            "type": "string"
        },
        {
            "metadata": {},
            "name": "_execution_id",
            "nullable": true,
            "type": "string"
        }
    ],
    "type": "struct"
}

// obtener solo los nombres de los campos
let fieldNames = fields.fields.map(field => field.name);
console.log(fieldNames);

// convierte el objeto en un archivo csv con fs
fs.writeFileSync('campos.csv', fieldNames.join('\n'));