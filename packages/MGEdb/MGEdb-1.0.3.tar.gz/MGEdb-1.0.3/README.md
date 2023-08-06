# MGEdb - Mobile Genetic Element database

MGEdb contains Mobile Genetic Elements sourced from several public databases
including RefSeq, Tn registry and ICEberg. The database contain information on
the properties, classification and genetic sequence of elements.

The database is shipped with a basic python API and a commandline interface for
interacting with and maintaining the database. While the database and API is
primarily desiged for the
[MGEfinder](https://bitbucket.org/mhkj/mgefinder/src/master/) tool other
applications are possible.

# Installation

The database APIs are developed for python 3.7+, other versions are not
activly supported.

Install database dependencies using the requirements file.

```bash
pip install -r requirements.txt
```

Run integration tests with either

```bash
make test
```

or

```bash
python setup.py test
```

# Database structure

The database information is stored in [mgedb/data](./mgedb/data). Database
records are stored in json format. MGE nucleotide sequences are stored in fasta
format in the folder [mgedb/data/seqeunces.d](./mgedb/data/sequences.d/).

# Database commands

To see the available commands.

```bash
mgedb --help
```

To view a single MGE record or all the records of a given family in the
database. Information are by default printed to stdout in a human readable
format. 

```bash
# view MGE record
mgedb view --name mge_name

# view all records from a given family
mgedb view --family mge_family_name
```

Extract CDS seqeunces and the sequences of the inverted repeats from MGE
sequences in the database. These commands extract the ranges that are annotated
in MGE records.

```bash
# Extract Inverted Repeat sequences annotated in MGEdb
mgedb extract ir output_file

# Extract CDS sequences for each MGE record with annotated CDS in MGEdb
mgedb extract ir output_file
```

## Commands for updating and maintaining the database

Validate that database content conforms to database schema.

```bash
mgedb validate
```

Backup database as a tarball.

```bash
mgedb backup
```

Update database with new records and sequences. The new information need to be
formatted in the MGEdb format. Prior to updating it makes an optional backup.
Use the flag `--dry-run` to test the update without changing the database files.

```bash
mgedb update /path/to/new_database
```

# Database API

Import and make database instance.

```python
from mgedb import MGEdb

db = MGEdb()

mge_records = db.records

insertion_sequence_26 = mge_records['IS26']
```

Iterate over database sequences.

```python
from mgedb import MGEdb

db = MGEdb()

mge_sequences = db.record_sequences
for mge in mge_sequences:
    header = mge.title
    sequence = mge.seq
```

See valid MGE names and MGE types in database

```python
from mgedb import MGEdb

db = MGEdb()

mge_type_abbreviation = db.nomenclature.keys()
valid_insertion_sequence_names = db.nomenclature['is']
```
