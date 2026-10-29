with transactions as (
    select * from {{ ref('stg_transactions') }}
),

owners as (
    select * from {{ ref('stg_pet_owners') }}
),

supplies as (
    select * from {{ ref('stg_pet_supplies') }}
)

select
    t.transaction_id,
    t.owner_id,
    t.supply_id,
    t.quantity,
    s.price,
    t.quantity * s.price as total_amount,
    t.status,
    t.created_at
from transactions t
join owners o on t.owner_id = o.owner_id
join supplies s on t.supply_id = s.supply_id
