with source as (
    select *
    from {{ source('raw_ecommerce', 'pet_owners') }}
),

renamed_and_cleaned as (
    select
        id as user_id,
        name as full_name,
        coalesce(email, 'unknown@example.com') as email,
        phone
    from source
)

select *
from renamed_and_cleaned