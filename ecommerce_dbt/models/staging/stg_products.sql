with source as (
    select *
    from {{ source('raw_ecommerce', 'pet_supplies') }}
),

cleaned as (
    select
        id as product_id,
        name as product_name,
        category,
        case
            when price < 0 then 0
            else price
        end as price,
        brand_id
    from source
)

select *
from cleaned