
select
    round(pickup_latitude, 2)   as pickup_lat_grid,
    round(pickup_longitude, 2)  as pickup_long_grid,
    count(*)                    as trip_count,
    sum(total_amount)           as total_revenue,
    round(avg(trip_distance), 2) as avg_trip_distance
from {{ ref('slv_taxi_trips') }}
where not (pickup_latitude = 0 and pickup_longitude = 0)
group by
    round(pickup_latitude, 2),
    round(pickup_longitude, 2)