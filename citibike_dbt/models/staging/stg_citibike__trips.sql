with source as (

    select * from {{ source('citibike', 'raw_tripdata') }}

),

renamed as (
    select
        cast(ride_id as varchar) as ride_id,
        cast(lower(trim(rideable_type)) as varchar) as rideable_type,
        try_to_timestamp_ntz(started_at) as started_at,
        try_to_timestamp_ntz(ended_at) as ended_at,
        cast(lower(trim(start_station_name)) as varchar) as start_station_name,
        cast(start_station_id as varchar) as start_station_id,
        cast(lower(trim(end_station_name)) as varchar) as end_station_name,
        cast(end_station_id as varchar) as end_station_id,
        cast(start_lat as float) as start_latitude,
        cast(start_lng as float) as start_longitude,
        cast(end_lat as float) as end_latitude,
        cast(end_lng as float) as end_longitude,
        cast(lower(trim(member_casual)) as varchar) as member_type,
        cast(_loaded_at as timestamp_ntz) as loaded_at

    from source

)

select * from renamed