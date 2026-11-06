with staging as 
(
    select 
        *
    from {{ ref('stg_citibike__trips') }}
),
transformed as 
(
    select
        ride_id,
        rideable_type,
        started_at,
        ended_at,
        cast(started_at as date) as started_at_date,
        cast(ended_at as date) as ended_at_date,
        coalesce(start_station_id, '-1') as start_station_key,
        coalesce(end_station_id, '-1') as end_station_key,
        member_type,
        loaded_at
    from staging
),
hashed as 
(
    select
        ride_id,
        {{ dbt_utils.generate_surrogate_key(['started_at_date']) }} as started_at_key,
        {{ dbt_utils.generate_surrogate_key(['ended_at_date']) }} as ended_at_key,
        {{ dbt_utils.generate_surrogate_key(['start_station_key']) }} as start_station_key,
        {{ dbt_utils.generate_surrogate_key(['end_station_key']) }} as end_station_key,
        rideable_type,
        started_at,
        ended_at,
        datediff('second', started_at, ended_at) as duration_in_sec,
        datediff('minute', started_at, ended_at) as duration_in_min,
        member_type,
        loaded_at
    from transformed
)
select
    *
from hashed
