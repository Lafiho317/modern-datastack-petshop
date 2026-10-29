with source as (
    select * from {{ source('raw_petshop', 'pet_supplies') }}
)

select
    supply_id,
    brand_id,
    supply_name,
    category,
    case when price < 0 then 0 else price end as price,
    is_active
from source
