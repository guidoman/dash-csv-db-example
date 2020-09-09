import os
from random import randrange

import numpy as np

from my_db import engine, my_data, meta, db_file_name


def main():
    if os.path.isfile(db_file_name):
        print('Sqlite DB file already exists. Delete it first if you want to generate new data.')
        exit()
    meta.create_all(engine)
    with engine.connect() as conn:
        for yyyymmdd in ['20200907', '20200908', '20200909']:
            # Generate random sinusoid data
            rnd_int = randrange(10, 100)
            t = np.linspace(0, rnd_int, rnd_int * 10)
            y = np.sin(t)
            # Convert data to CSV lines with header
            csv_header = 'x,y'
            csv_data = '\n'.join(f'{a},{b}' for a, b in zip(t, y))
            csv = csv_header + '\n' + csv_data
            # Insert into DB
            ins = my_data.insert().values(yyyymmdd=yyyymmdd, csv=csv)
            conn.execute(ins)


if __name__ == '__main__':
    main()
