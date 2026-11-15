# Data directory

Place the official OSHA Severe Injury Reports CSV at:

`data/raw/January2015toNovember2025.csv`

The raw data directory is excluded from Git. The deployable ZIP does not redistribute the raw source CSV. Download the current extract from the official OSHA Severe Injury Reports page and keep it locally. The raw file is excluded from Git because it contains establishment, location and narrative fields. The packaged operational model can run the app without the CSV.
