- File created: 11/02/23
- Authors: Kai Barber-Harris
- Reviewers: 
- Last review date: 
- Review comments: 

# Overview
The project needs to have a well-formatted database of locations of water fountains, bins, food shops, and bus stops.
Each type of location should be stored in one or multiple databases/files which should be kept server-side and sent when the app is opened.
Each location should ideally have associated geolocation data attached for later use.

# Methodology
## Data collection
The information we need to gather will likely need to be gathered manually; however, for our purposes, we only need to provide a sample.
Collect three (3) to five (5) examples of each location, and record their information in a JSON file. 
We can store all the locations in a single JSON file, which are data-only. 
If this single file later becomes an issue (e.g. needing to only read 1 type of location), it should be relatively simple to split this list into multiple JSON files.
For now, I think the simplicity of a single file should be preferred.

## JSON snippet
```json
{

  "Fountains" : [
    {
    "Name" : "Example name 1",
    "Location" : "Description of location 1",
    "Geolocation" : "Latitude, Longitude",
    "Other information" : "A note about Location 1",
    "Report references" : "#1, #2"
    },
    {
    "Name" : "Example name 2",
    "Location" : "Description of location 2",
    "Geolocation" : "Latitude, Longitude",
    "Other information" : "A note about Location 2",
    "Report references" : "#3, #4"
    }
  ]
  
}
```
Naturally, there should be lists for all 4 types of location. 
This is reflected in the `locations.json` file already created in the root directory; this may need to be moved to be inside the Django server when it is created.
The data collection should simply be made directly into `locations.json`.

## Field explanation
- Name: Every location should have a unique name to be able to identify it quickly and easily.
- Location: The textual description of the location is the unique part of our idea.
- Geolocation: Exact geolocation data should be useful in providing recommendations on nearby fountains, bins, etc.
- Other information: Placeholder field for gamekeepers to provide other information about the location e.g. noting broken fountains, providing repair dates, warning of a removal
- Report references: It may be useful to keep references to reports in the JSON data. This way, reports can be quickly related directly to locations, as there is a many-to-one relation between them.

## Other notes
- Other fields may need to be added later; we should try to think of all possible data we might need and plan to have it. It's easier to cut or not use extraneous data than retrofit our design later on to accommodate for new fields.
- The `locations.json` file may need to be moved inside the server's filestructure.
- An alternative to a `json` file is a `csv`. I opted for `json` as I personally prefer the structuring of data and believe it should be more robust.
- Upon data collection, `"Report references"` should be empty, as no reports have been generated yet.
- Similarly, `"Other information"` may be left blank at the discretion of the data collector.
- A mapping app on your phone should provide sufficiently accurate geolocation data, especially as it will be phone geolocation data we are comparing to later on.
- It may be possible to program a system which checks if a new update has been made to `locations.json`, allowing us to only send the database once and whenever it is updated instead of every time the app is opened.
  - This is an extremely small improvement, likely only saving a few hundred KB of data per open.
  - This would lend itself to splitting `locations.json` into a set of unique `json` files, so we only send the file which has been updated.
  - An optimisation we could make at the end of the project to show off, if we have time.
- Depending on how Django implements databases and stores their information, having our own `json` may be overkill and useless. However, it provides a rigid framework in which we can collect data, which plays nicely with Python, Java, and C.
