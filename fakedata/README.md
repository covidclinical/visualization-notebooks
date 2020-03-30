### Fake data

The data contained in this directory has been created for the purposes of preparing visualizations while real data from real sites is gathered.

Fake site-level files here should have the expected formats:
- CSV
- no headers
- generated according to the `site_level_data/{site_id}/{year}-{month}-{day}_{file_type}-{site_id}.csv` convention, where `{file_type}` is one of 
    - `DailyCounts`
    - `Demographics`
    - `Diagnoses`
    - `Labs`
- file contents should match those described [here](https://github.com/GriffinWeber/covid19i2b2/blob/master/COVID19_Data_Files_Description.txt)

To avoid confusion, it may be helpful to use fake site IDs where possible (e.g. `FMC` for "fake medical center", `FCH` for "fake children's hospital")

Scripts / notebooks used to generate fake data can be stored in `src/`.