Bicycles! Scrapers! :cow::dog: Moof!

# Endpoints

## Database

* `/db/setup` - sets up a database when run on a clean local enviroment 
* `/db/test` - writes a test record in the database. **Don't forget to remove!**

## API

* `/api/1/<service>/stations` - fetches all stations of the specified service. 
* `/api/1/<service>/statistics?station_ids=[a,b]&time_ranges=[0-10,50-100]` - fetches statistics of the specified service. See statistics for more details. 

**Deprecated**

* `/api/1/<service>/scrape` - triggers scraping of the selected service. Normally performed by cron task. 

# Statistics

```javascript
{
  "response": {
    "statistics": [
      {
        "stations": {
          "121": csv_data,
          "343": csv_data
        },
        "service": "telofun"
      }
    ]
  }
}
```

Where `csv_data` is `samples_count`, `available_docks`, `hour_of_week`, `available_bicycles`

# Utility

## Getting app quota

```bash
$ rhc show-app bicycle --gears quota
```