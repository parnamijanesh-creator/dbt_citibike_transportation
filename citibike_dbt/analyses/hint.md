### Table 3.3: `fct_trips` (Fact Table)

* **Model Classification:** Transaction Fact Table.
* **Declared Grain:** Exactly **one row per completed individual bike trip**.

| Column Name             | Physical Data Type       | Key / Attribute Classification | Description & Provenance (Artifact 3 Lineage)                                             |
| :---------------------- | :----------------------- | :----------------------------- | :---------------------------------------------------------------------------------------- |
| `ride_id`               | `VARCHAR(255) NOT NULL`  | **Primary Key** (Natural Key)  | Natural primary key of the physical ride event (Artifact 2 Section 2).                    |
| `start_station_key`     | `VARCHAR(32) NOT NULL`   | **Foreign Key** (Role-Playing) | Departure station key joining to `dim_stations.station_key` (Policy 4.2b).                |
| `end_station_key`       | `VARCHAR(32) NOT NULL`   | **Foreign Key** (Role-Playing) | Arrival station key joining to `dim_stations.station_key` (Policy 4.2b).                  |
| `start_date_key`        | `DATE NOT NULL`          | **Foreign Key** (Role-Playing) | Departure date key joining to `dim_date.date_key` (Canonical anchor) (Policy 4.4b).       |
| `end_date_key`          | `DATE NOT NULL`          | **Foreign Key** (Role-Playing) | Arrival date key joining to `dim_date.date_key` (Role-playing anchor) (Policy 4.4b).      |
| `membership_type`       | `VARCHAR(20) NOT NULL`   | **Degenerate Dimension**       | Rider subscription tier: `'member'` vs. `'casual'` (Entry 1).                             |
| `rideable_type`         | `VARCHAR(50) NOT NULL`   | **Degenerate Dimension**       | Vehicle classification: `'classic_bike'` vs. `'electric_bike'` (Artifact 2 Section 5.1).  |
| `started_at`            | `TIMESTAMP_NTZ NOT NULL` | **Event Timestamp**            | Exact physical departure timestamp (Policy 4.1a).                                         |
| `ended_at`              | `TIMESTAMP_NTZ NOT NULL` | **Event Timestamp**            | Exact physical arrival timestamp (Policy 4.1a).                                           |
| `start_hour`            | `INTEGER NOT NULL`       | **Intraday Event Attribute**   | Clock hour integer $0 \text{ to } 23$ extracted from `started_at` (Policy 4.4a).          |
| `time_of_day_bucket`    | `VARCHAR(30) NOT NULL`   | **Degenerate Dimension**       | Commute partition: `'Morning Commute'`, `'Midday / Afternoon'`, etc. (Policy 4.4a).       |
| `is_rush_hour`          | `BOOLEAN NOT NULL`       | **Degenerate Flag**            | Weekday peak commute flag ($7\text{--}9\text{ AM}, 4\text{--}6\text{ PM}$) (Policy 4.4a). |
| `is_sub_minute_trip`    | `BOOLEAN NOT NULL`       | **Degenerate Outlier Flag**    | False start indicator for rides lasting $< 60\text{ seconds}$ (Policy 4.1b).              |
| `is_extreme_duration`   | `BOOLEAN NOT NULL`       | **Degenerate Outlier Flag**    | Forgotten return indicator for rides lasting $> 24\text{ hours}$ (Policy 4.1b).           |
| `is_round_trip`         | `BOOLEAN NOT NULL`       | **Degenerate Geometry Flag**   | Indicator for trips where `start_station_id = end_station_id` (Policy 4.3b).              |
| `duration_seconds`      | `INTEGER NOT NULL`       | **Additive Fact Measure**      | Exact physical ride duration in seconds (Policy 4.1b).                                    |
| `duration_minutes`      | `NUMERIC(10,2) NOT NULL` | **Additive Fact Measure**      | Exact ride duration in decimal minutes (Policy 4.1b).                                     |
| `estimated_distance_km` | `NUMERIC(10,3) NULL`     | **Additive Fact Measure**      | Haversine distance; set to `NULL` for round trips or missing GPS (Policy 4.3b).           |