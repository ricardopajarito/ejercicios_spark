import os
from urllib.parse import urlparse
from uuid import uuid4

def _parse_s3_uri(uri):
    p = urlparse(uri)
    return p.netloc, p.path.lstrip('/')

def convert_each_csv_to_named_parquet(s3_client, spark, csv_s3_uris, target_s3_prefix):
    # target_s3_prefix: ej. "s3://bucket/ingest/nsccap_pq/refventas/"
    target_bucket, target_prefix = _parse_s3_uri(target_s3_prefix)

    for csv_uri in csv_s3_uris:
        src_bucket, src_key = _parse_s3_uri(csv_uri)
        base_name = os.path.splitext(os.path.basename(src_key))[0]    # original filename sin extensión
        final_key = f"{target_prefix}{base_name}.parquet"             # destino final: <prefix>/<name>.parquet

        # 1) Leer CSV individualmente
        df = spark.read.option("header", True).option("inferSchema", True).csv(csv_uri)

        # 2) Escribir parquet en prefijo temporal (forzar 1 archivo parquet)
        temp_uuid = str(uuid4())
        temp_prefix = f"{target_prefix}tmp/convert-{temp_uuid}/"
        temp_s3_uri = f"s3://{target_bucket}/{temp_prefix}"
        df.coalesce(1).write.mode("overwrite").parquet(temp_s3_uri)

        # 3) Encontrar el part-*.parquet dentro del prefijo temporal
        resp = s3_client.list_objects_v2(Bucket=target_bucket, Prefix=temp_prefix)
        part_key = None
        for obj in resp.get("Contents", []):
            k = obj["Key"]
            if k.endswith(".parquet") and "part-" in os.path.basename(k):
                part_key = k
                break
        if not part_key:
            raise RuntimeError(f"No se encontró archivo parquet en {temp_s3_uri}")

        # 4) Copiar el part-*.parquet al destino final con nombre derivado del CSV
        copy_source = {"Bucket": target_bucket, "Key": part_key}
        s3_client.copy_object(Bucket=target_bucket, CopySource=copy_source, Key=final_key)

        # 5) Opcional: eliminar objetos temporales (part y _SUCCESS)
        to_delete = [{"Key": o["Key"]} for o in resp.get("Contents", [])]
        if to_delete:
            s3_client.delete_objects(Bucket=target_bucket, Delete={"Objects": to_delete})

        print(f"Convertido {csv_uri} -> s3://{target_bucket}/{final_key}")