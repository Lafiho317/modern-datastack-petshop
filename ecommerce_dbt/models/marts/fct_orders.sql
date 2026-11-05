{{ config(materialized='table') }}

select
    o.order_id,
    o.user_id,
    o.product_id,
    o.quantity,
    o.created_at,
    o.quantity * p.price as total_amount
from {{ ref('stg_orders') }} o
join {{ ref('stg_users') }} u
    on o.user_id = u.user_id
join {{ ref('stg_products') }} p
    on o.product_id = p.product_id