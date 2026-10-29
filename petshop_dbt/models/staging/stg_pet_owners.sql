with source as (
    select * from {{ source('raw_petshop', 'pet_owners') }}
),

deduplicated as (
    select
        *,
        row_number() over (
            partition by owner_id
            order by registration_date desc
        ) as rn
    from source
)

select
    owner_id,
    full_name,
    coalesce(email, 'unknown@example.com') as email,
    city,
    pet_type,
    cast(registration_date as date) as registration_date
from deduplicated
where rn = 1
