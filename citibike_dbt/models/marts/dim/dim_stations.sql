with staging as 
(
    select *
    from {{ ref('stg_citibike__trips') }}
),
unioned_stations as 
(
    select
        start_station_id as station_id,
        start_station_name as station_name,
        start_latitude as station_latitude,
        start_longitude as station_longitude
    from staging
    where start_station_id is not null
    union all
    select
        end_station_id as station_id,
        end_station_name as station_name,
        end_latitude as station_latitude,
        end_longitude as station_longitude
    from staging
    where end_station_id is not null
),
aggregated_stations as 
(
    select
        station_id,
        max(station_name) as station_name,
        round(avg(station_latitude), 6) as station_latitude,
        round(avg(station_longitude),6) as station_longitude
    from unioned_stations
    group by 1
),
unioned as 
(
    select 
        '-1' as station_id,
        'Unassigned / Dockless Station' as station_name,
        cast(null as float) as station_latitude,
        cast(null as float) as station_longitude
    union all

    select *
    from aggregated_stations
),
final as (
    select 
        {{ dbt_utils.generate_surrogate_key(['station_id']) }} as station_key,
        *
    from unioned
)
select *
from final