# Data dictionary (Week 0, Saturday)

Two datasets I will use in this program. For each one: where it came from, what one row means, and what each column means.

**Sources of meanings:** the taxi meanings are written in my own words from the official [TLC Yellow Taxi data dictionary](https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf). Code lists (payment type, rate code) should be double-checked against that PDF. The World Bank meanings come from the files inside the ZIP and from checks I ran on the data.

---

## 1. NYC yellow taxi trips, January 2026 (Parquet)

- **Source:** <https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2026-01.parquet>
- **Downloaded:** October 2, 2026
- **Rows / size:** 3,724,889 rows / 64.2 MB / 20 columns
- **One row represents:** **one yellow-taxi trip, from the moment the meter starts to the moment it stops.**
- **Careful:** there is no trip ID column, so I cannot prove from the columns alone that no trip is listed twice.

### Example row (row 1)

| Column | Value |
| --- | --- |
| VendorID | 2 |
| tpep_pickup_datetime | 2026-01-01 00:54:04 |
| tpep_dropoff_datetime | 2026-01-01 00:59:37 |
| passenger_count | 1 |
| trip_distance | 0.97 |
| PULocationID / DOLocationID | 239 / 238 |
| payment_type | 1 |
| fare_amount | 7.2 |
| tip_amount | 3.66 |
| total_amount | 15.86 |

Reading it in plain words: a 0.97-mile trip that lasted about 5.5 minutes, from zone 239 to zone 238, paid by one passenger, total 15.86 dollars including a 3.66 tip.

### Columns

| Column | Type | Meaning (plain words) | Nulls | Notes |
| --- | --- | --- | --- | --- |
| VendorID | INTEGER | Which taxi-technology company supplied the record (a code: 1, 2, 6 or 7). | 0.0% | 4 distinct values |
| tpep_pickup_datetime | TIMESTAMP | When the meter was switched on, so when the trip started. | 0.0% | Min 2025-12-31 23:57:29, max 2026-02-01 00:45:01, so a few trips fall outside January |
| tpep_dropoff_datetime | TIMESTAMP | When the meter was switched off, so when the trip ended. | 0.0% | Max 2026-02-01 23:35:31 |
| passenger_count | BIGINT | Number of passengers, entered by the driver. | 29.2% | 0 appears, which is probably a missing value typed as 0 |
| trip_distance | DOUBLE | Distance of the trip in miles, from the meter. | 0.0% | Max 269,097 miles is impossible, so it is bad data |
| RatecodeID | BIGINT | The type of rate used at the end of the trip (standard, airport, negotiated, group ride...). A code. | 29.2% | Value 99 appears; check the PDF for what it means |
| store_and_fwd_flag | VARCHAR | Y or N: was the trip saved in the car's memory before being sent, because the car had no connection? | 29.2% | |
| PULocationID | INTEGER | The taxi zone where the trip started (**P**ick**U**p). An ID number; the names are in the TLC taxi zone lookup table. | 0.0% | Max 265 |
| DOLocationID | INTEGER | The taxi zone where the trip ended (**D**rop**O**ff). | 0.0% | Max 265 |
| payment_type | BIGINT | How the passenger paid. A code (for example card, cash, no charge, dispute). | 0.0% | Values 0 to 4 appear |
| fare_amount | DOUBLE | Fare worked out by the meter from time and distance, in US dollars. | 0.0% | Negative values exist (min -2555.2), possibly refunds or corrections |
| extra | DOUBLE | Extra charges added to the fare, such as rush-hour or overnight charges. | 0.0% | |
| mta_tax | DOUBLE | A tax for the regional transport authority, added automatically. | 0.0% | |
| tip_amount | DOUBLE | The tip. Recorded automatically for card payments; cash tips are not included. | 0.0% | Max 766.0 looks suspicious |
| tolls_amount | DOUBLE | Total of all tolls paid during the trip. | 0.0% | |
| improvement_surcharge | DOUBLE | A fixed surcharge added at the start of the trip. | 0.0% | |
| total_amount | DOUBLE | The total charged to the passenger. Cash tips are not included. | 0.0% | Not always the sum of all charge columns (see below) |
| congestion_surcharge | DOUBLE | New York State charge for congestion. | 29.2% | |
| Airport_fee | DOUBLE | A fee for pickups at the airports. | 29.2% | |
| cbd_congestion_fee | DOUBLE | The MTA charge for trips in the Congestion Relief Zone, which started in 2025. | 0.0% | |

### Things to watch

1. **Five columns have exactly 29.2% nulls:** `passenger_count`, `RatecodeID`, `store_and_fwd_flag`, `congestion_surcharge` and `Airport_fee`. That suggests the same rows are missing all five. To check in Week 1.
2. **Negative amounts** exist in most money columns. Decide in Week 1 whether to keep, flag or remove them.
3. **Impossible values** such as a 269,097-mile trip.
4. **The file is not a clean calendar month:** pickups run from Dec 31 to Feb 1.
5. **`total_amount` is not always the sum of the parts.** In my sample rows 2 and 3 it leaves out the congestion surcharge and the CBD fee, while row 1 includes the 2.5. Test this on all rows in Week 1.
6. **`~distinct` in the profile is approximate.** For example, PULocationID shows about 290 distinct but its maximum is 265, so there can be at most 265 zones.

### Questions this data could answer

1. Which pickup zones have the most trips, and at what hours of the day?
2. What share of trips are paid by card versus cash, and how do average fares compare?
3. How are trip duration (from pickup and drop-off times), distance and fare related?

---

## 2. World Bank indicators for Cameroon (CSV)

- **Source:** <https://api.worldbank.org/v2/en/country/CMR?downloadformat=csv>
- **Downloaded:** October 2, 2026 (file says "Last Updated Date: 2026-07-13")
- **File used:** `API_CMR_DS2_en_csv_v2_418102.csv` (read with the first 4 description lines skipped)
- **Rows / size:** 1,498 rows / 980.7 KB / 70 columns (66 year columns, 4 label columns, 1 empty column)
- **One row represents:** **one indicator (one kind of measurement) for Cameroon, with its values for every year from 1960 to 2025 spread across the columns.**
- **Checked:** the file has 1,498 rows and 1,498 different indicator codes, so no indicator appears twice, and only one country (CMR).

### What "wide" means (the key idea)

This table is **wide**: years run across as columns. Think of a school report card where each subject is a row and each year is a column. A **long** table would instead have one row per indicator **and** year, for example `Population, total | 2020 | 26,210,558`. Many analysis tools prefer long tables, so later we will turn this one into long format.

Example, the same column `2020` for four different rows:

| Indicator | Value in 2020 |
| --- | --- |
| Intentional homicides (per 100,000 people) | 4.59 |
| Life expectancy at birth, total (years) | 61.67 |
| Population, total | 26,210,558 |
| GDP (current US$) | 40,773,241,177 |

The numbers have completely different units, so the column statistics for the year columns (min, max, distinct) mean nothing. Always read an indicator's own row.

### Columns

| Column | Type | Meaning (plain words) | Nulls | Notes |
| --- | --- | --- | --- | --- |
| Country Name | VARCHAR | Name of the country. | 0.0% | Always "Cameroon" |
| Country Code | VARCHAR | Three-letter code of the country. | 0.0% | Always "CMR" |
| Indicator Name | VARCHAR | What is being measured, in words (e.g. "Population, total"). | 0.0% | 1,498 different values, one per row |
| Indicator Code | VARCHAR | A short unique code for the measure (e.g. SP.POP.TOTL). | 0.0% | Unique per row (checked) |
| 1960 ... 2025 (66 columns) | DOUBLE | The value of that row's indicator in that year. The unit depends on the row (people, US dollars, percent, years...). | About 24% to 89% per column | Overall only about 44.6% of the cells have a value; older years are mostly empty |
| column70 | VARCHAR | An empty column created by a trailing comma at the end of each line. | 100.0% | Ignore it |

### Things to watch

1. **117 of the 1,498 rows have no value in any year.** These indicators exist but have no data for Cameroon.
2. **Missing values** are very common: about 55% of the year cells are empty.
3. **Mixed units** in the same column (see the table above).
4. **Meanings and sources of each indicator** are in the second file of the ZIP, `Metadata_Indicator_...csv`, with the columns `INDICATOR_CODE`, `INDICATOR_NAME`, `SOURCE_NOTE` and `SOURCE_ORGANIZATION`.
5. **Country facts** are in `Metadata_Country_...csv`: region "Sub-Saharan Africa", income group "Lower middle income".

### Questions this data could answer

1. How has Cameroon's population changed from 1960 to 2025?
2. How have GDP and life expectancy moved since the year 2000?
3. Which indicators have the most missing years, and are they linked to particular topics?
