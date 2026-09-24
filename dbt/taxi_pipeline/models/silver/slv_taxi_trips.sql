with source as (

    select * from {{ source('bronze', 'brz_taxi_trips') }}

),

typed as (

    select
        sha2(
            concat_ws(
                '|',
                VendorID, tpep_pickup_datetime, tpep_dropoff_datetime,
                pickup_longitude, pickup_latitude, dropoff_longitude, dropoff_latitude
            ),
            256
        ) as trip_id,
        cast(VendorID as int)                          as vendor_id,
        cast(tpep_pickup_datetime as timestamp)         as pickup_datetime,
        cast(tpep_dropoff_datetime as timestamp)        as dropoff_datetime,
        cast(passenger_count as int)                    as passenger_count,
        cast(trip_distance as decimal(10, 2))           as trip_distance,
        cast(pickup_longitude as decimal(10, 7))        as pickup_longitude,
        cast(pickup_latitude as decimal(10, 7))         as pickup_latitude,
        cast(dropoff_longitude as decimal(10, 7))       as dropoff_longitude,
        cast(dropoff_latitude as decimal(10, 7))        as dropoff_latitude,
        cast(RatecodeID as int)                         as rate_code_id,
        store_and_fwd_flag,
        cast(payment_type as int)                       as payment_type,
        cast(fare_amount as decimal(10, 2))             as fare_amount,
        cast(extra as decimal(10, 2))                   as extra,
        cast(mta_tax as decimal(10, 2))                 as mta_tax,
        cast(tip_amount as decimal(10, 2))              as tip_amount,
        cast(tolls_amount as decimal(10, 2))             as tolls_amount,
        cast(improvement_surcharge as decimal(10, 2))   as improvement_surcharge,
        cast(total_amount as decimal(10, 2))            as total_amount
    from source

),

deduplicated as (

    select *
    from typed
    qualify row_number() over (partition by trip_id order by pickup_datetime) = 1

)

select
    trip_id, vendor_id, pickup_datetime, dropoff_datetime, passenger_count,
    trip_distance, pickup_longitude, pickup_latitude, dropoff_longitude, dropoff_latitude,
    rate_code_id, store_and_fwd_flag, payment_type, fare_amount, extra, mta_tax,
    tip_amount, tolls_amount, improvement_surcharge, total_amount
from deduplicated
where
    trip_distance >= 0
    and fare_amount >= 0
    and pickup_datetime is not null
    and dropoff_datetime is not null