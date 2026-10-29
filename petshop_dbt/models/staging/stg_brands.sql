select
    brand_id,
    brand_name,
    country
from {{ source('raw_petshop', 'brands') }}
