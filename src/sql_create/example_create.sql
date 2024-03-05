CREATE OR REPLACE VIEW {TARGET_DATABASE_TPL}.my_dest_table AS
WITH example AS (
    SELECT id
        , cast(min(creation_date) as date) min_creation_date
        , cast(max(updated_date) as date) max_updated_date
    FROM {RAW_DATABASE}.my_src_table
    GROUP BY id
)
SELECT *
FROM example