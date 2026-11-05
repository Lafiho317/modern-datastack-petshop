{{ config(materialized='table') }}

select
    user_id,
    full_name,
    email,
    phone
from {{ ref('stg_users') }}