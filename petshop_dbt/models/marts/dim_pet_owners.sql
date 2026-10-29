select
    owner_id,
    full_name,
    email,
    city,
    pet_type,
    registration_date
from {{ ref('stg_pet_owners') }}
