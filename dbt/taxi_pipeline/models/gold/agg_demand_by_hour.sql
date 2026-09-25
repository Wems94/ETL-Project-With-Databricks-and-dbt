
with trips as (

    select * from {{ ref('slv_taxi_trips') }}

)

select
    date(pickup_datetime)                       as pickup_date,
    dayofweek(pickup_datetime)                  as pickup_day_of_week,
    date_format(pickup_datetime, 'EEEE')        as pickup_day_name,
    hour(pickup_datetime)                       as pickup_hour,
    count(*)                                    as trip_count,
    sum(total_amount)                           as total_revenue,
    round(avg(total_amount), 2)                 as avg_revenue_per_trip,
    round(avg(trip_distance), 2)                as avg_trip_distance
from trips
group by
    date(pickup_datetime),
    dayofweek(pickup_datetime),
    date_format(pickup_datetime, 'EEEE'),
    hour(pickup_datetime)