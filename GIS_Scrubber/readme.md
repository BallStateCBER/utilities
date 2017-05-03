# GIS Scrubber

### Purpose:
**Provide a method for automatically formatting data properly for GIS use.**
GIS is picky about the way data files and headers are named.
It also likes to crash if these conventions aren't followed, which is annoying.

### Supported file types:
- csv-like files (`.csv`, `.tsv`, `.txt`)
- newer Excel files (`.xlsx`)
  - **_warning_**: due to the renaming of worksheets, sheet references in formulas may break.

### Requirements:
- python
- openpyxl

(see `requirements.txt`)

### Basic Usage:
- Place the files to be scrubbed into the "dirty" directory.
- Run scrub_dirty_data.bat

**Make sure to remove any blank rows at the top of your data!**
(These will break GIS on import, but the tool doesn't notice these errors.)


### Advanced Usage:
`python gis_scrubber.py -d <dirty-directory> -c <clean-directory>`
(for custom input/output locations)
