PROCESS

1) Generate KAF files with OpeNER using ner-batch.sh
2) Turn KAF files into KWIC files that contain every 'location' entity and its keyword in context using "KafNafParser.py"
3) Merge KWIC files by year using "Merge KWICs on YEAR.py"
4) Clean yearly KWIC files
5) Aggregate cleaned KWIC files using "Aggregate the Results.py"
6) Generate a master location list for use in geocoding using "Master List for Geocoding.py"
7) Geocode the master list using "Geocode-Master-Location-List.py"
8) Use this geocoded master list as a look-up to code each aggregate file using "Geocode-Local-Lookup.py"
9) Generate maps using "Visualizing-Empire_map-test_fork_point-list-explosion.py"