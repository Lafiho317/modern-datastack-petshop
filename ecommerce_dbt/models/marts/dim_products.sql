{{ config(materialized='table') }}

select
    p.product_id,
    p.product_name,
    p.category,
    p.price,
    b.name as brand_name
from {{ ref('stg_products') }} p
left join {{ source('raw_ecommerce', 'brands') }} b
    on p.brand_id = b.id