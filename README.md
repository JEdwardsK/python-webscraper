# python web scraper



Practice using bs4 to build a web scraper. 

The function `update_film_json` takes url from AMC Theatres and creates a data.json file that collates the films show times and information for the next 7 days.

the url is from the get all show times after selecting a location and clicking get tickets

JSON structure:

```typescript
  [
    {
      filmName: string,
      href: string,
      screens: {
        day0?: [
          {
            screenType: string,
            screenFeatures: string[],
            showTimes: [
              {
                time: string,
                href: string
              }
            ]
          }
        ],
        day1?:[], // same shape as day0, if films are showing on that day
        day2?:[], // ibid
        day3?:[],
        day4?:[],
        day5?:[],
        day6?:[],
        day7?:[]
      }
    }
  ]
