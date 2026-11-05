with source as (
    select *
    from {{ source('raw_ecommerce', 'transactions') }}
)

select
    id as order_id,
    owner_id as user_id,
    supply_id as product_id,
    quantity,
    cast(transaction_date as timestamp) as created_at
from source