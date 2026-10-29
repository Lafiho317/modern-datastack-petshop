with supplies as (
    select * from {{ ref('stg_pet_supplies') }}
),

brands as (
    select * from {{ ref('stg_brands') }}
)

select
    s.supply_id,
    s.supply_name,
    s.category,
    s.price,
    s.is_active,
    b.brand_name,
    b.country as brand_country
from supplies s
left join brands b on s.brand_id = b.brand_id
