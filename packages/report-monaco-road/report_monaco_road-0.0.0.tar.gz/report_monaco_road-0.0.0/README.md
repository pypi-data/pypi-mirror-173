# Task 6 - Report of Monaco 2018 Racing
This module read data from 2 files, order racers by time and print report that shows the top 15 racers and the rest after underline.
## Examples:
#### Shows list of drivers and by asc:
```bash
python3.8 -m report_monaco.app --files Road_data/ --asc
```
#### Return:
```
1. Sebastian Vettel  | FERRARI  | 0:01:04.415000
2. Valtteri Bottas  | MERCEDES  | 0:01:12.434000
3. Stoffel Vandoorne  | MCLAREN RENAULT  | 0:01:12.463000
.......
```
#### Shows list of drivers order by desc:
```bash
python3.8 -m report_monaco.app --files Road_data/ --desc
```
#### Return:
```
1. Kevin Magnussen  | HAAS FERRARI  | 0:01:13.393000
2. Lance Stroll  | WILLIAMS MERCEDES  | 0:01:13.323000
3. Marcus Ericsson  | SAUBER FERRARI  | 0:01:13.265000
.......
```

#### Shows statistic about driver:
```bash
python3.8 -m report_monaco.app --files Road_data/ --driver "Kevin Magnussen"
```
#### Return:
```
1. Kevin Magnussen  | HAAS FERRARI  | 0:01:13.393000
```