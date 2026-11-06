with date_spine as (
    {{ 
    dbt_utils.date_spine(
    datepart="day",
    start_date="cast('2023-12-31' as date)",
    end_date="cast('2027-01-01' as date)"
   )
}}
),
date_indicators as(
    select
        date_day,
        extract(year from date_day) as year,
        extract(month from date_day) as month,
    DECODE(EXTRACT(dayofweek_iso FROM date_day),
  1, 'Monday',
  2, 'Tuesday',
  3, 'Wednesday',
  4, 'Thursday',
  5, 'Friday',
  6, 'Saturday',
  7, 'Sunday') AS day_name,
    extract(dayofweek_iso from date_day) as weekday_iso,
    CASE
        WHEN dayofweekiso(date_day) in (6,7) THEN TRUE
        ELSE FALSE
    END as is_weekend
from date_spine
),
final as 
(
    select
        {{ dbt_utils.generate_surrogate_key(['date_day']) }} as date_key,
        *
    from date_indicators
)

select * from final