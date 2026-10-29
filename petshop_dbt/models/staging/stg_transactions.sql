select
    transaction_id,
    owner_id,
    supply_id,
    quantity,
    status,
    cast(transaction_date as timestamp) as created_at
from {{ source('raw_petshop', 'transactions') }}
