
with trips as (

    select * from {{ ref('slv_taxi_trips') }}

)

select
    payment_type,
    count(*)                                                          as trip_count,
    sum(tip_amount)                                                   as total_tips,
    round(avg(tip_amount), 2)                                         as avg_tip_amount,
    round(avg(case when fare_amount > 0 then tip_amount / fare_amount end) * 100, 2)
                                                                       as avg_tip_pct_of_fare
from trips
group by payment_type

