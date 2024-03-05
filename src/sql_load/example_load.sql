MERGE INTO {TARGET_DATABASE_TPL}.my_dest_iceberg_table AS t
USING {RAW_DATABASE}.my_src_iceberg_table as s
ON t.col1 = s.col1
WHEN NOT MATCHED
THEN INSERT (col1)
      VALUES (s.col1)