import json
from datetime import datetime
import matplotlib.pyplot as plt
import cartopy
import cartopy.feature as cpf
import numpy.random as npr
import cartopy.crs as ccrs
import sys, getopt
from datetime import datetime

def unix_ms_to_date(ms):
    return datetime.utcfromtimestamp(ms / 1000).strftime('%Y-%m-%d %H:%M:%S')

def main(argv):

    try:
        opts, args = getopt.getopt(argv, "f", ["file="])
        
        if len(opts) == 0 or opts[0][0] not in ("-f", "--file"):
            print("No file argument specified, plase specify with -f or --file=")
            sys.exit(2)

        else:
            if opts[0][0] == "-f":
                filepath = args[0]
            elif opts[0][0] == "--file":
                filepath = opts[0][1]
            else:
                print("Could not parse file. Please specify file with -f or --file=")
                sys.exit(2)
            print("File path is:", filepath)

        with open(filepath, 'r') as myfile:
            data=myfile.read()

        history_json = json.loads(data)

        latitudes = {}
        longtitudes = {}

        for location in history_json["locations"]:
            latitudes[int(location["timestampMs"])] = int(location["latitudeE7"]) / 1e+7
            longtitudes[int(location["timestampMs"])] = int(location["longitudeE7"]) / 1e+7
        
        print("Finished importing coordinates, generating coordinate array for matplotlib...")
        print("First datapoint is from", unix_ms_to_date(int(history_json["locations"][0]["timestampMs"])))
        print("Last datapoint is from", unix_ms_to_date(int(history_json["locations"][-1]["timestampMs"])))

        pts_x = []
        pts_y = []

        for timestamp in latitudes.keys():
            x_pt, y_pt = longtitudes[timestamp], latitudes[timestamp]
            pts_x.append(x_pt)
            pts_y.append(y_pt)

        proj = cartopy.crs.PlateCarree()

        print("Finished generating coordinate arrays, plotting values...")

        ax = plt.figure().gca(projection=proj)

        ax.add_feature(cpf.LAND)
        ax.add_feature(cpf.OCEAN)
        ax.add_feature(cpf.COASTLINE)
        ax.add_feature(cpf.BORDERS, linestyle=':')
        ax.add_feature(cpf.LAKES,   alpha=0.5)
        ax.add_feature(cpf.RIVERS)

        ax.scatter(pts_x, pts_y, transform=proj, s=1.5, c='orange')

        plt.show()

    except getopt.GetoptError:
        print("Could not parse file. Please specify file with -f or --file=")
        sys.exit(2)

if __name__ == "__main__":
   main(sys.argv[1:])