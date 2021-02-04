import json
from datetime import datetime
import matplotlib.pyplot as plt
import cartopy
import cartopy.feature as cpf
import numpy.random as npr
import cartopy.crs as ccrs
import sys, getopt
from datetime import datetime
import numpy as np

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
        print("First data point is from", unix_ms_to_date(int(history_json["locations"][0]["timestampMs"])))
        print("Last data point is from", unix_ms_to_date(int(history_json["locations"][-1]["timestampMs"])))
        print("Total amount of data points:", len(latitudes))

        pts_x = []
        pts_y = []

        for timestamp in latitudes.keys():
            x_pt, y_pt = longtitudes[timestamp], latitudes[timestamp]
            pts_x.append(x_pt)
            pts_y.append(y_pt)

        proj = cartopy.crs.PlateCarree()

        print("Finished generating coordinate arrays, plotting values...")

        fig = plt.figure()
        ax = fig.gca(projection=proj)

        ax.add_feature(cpf.LAND)
        ax.add_feature(cpf.OCEAN)
        ax.add_feature(cpf.COASTLINE)
        ax.add_feature(cpf.BORDERS, linestyle=':')
        ax.add_feature(cpf.LAKES,   alpha=0.5)
        ax.add_feature(cpf.RIVERS)

        annotations = []

        def onpick(event):
            global annotation
            index = event.ind[0]
            selected_lat = pts_y[index]
            selected_lon = pts_x[index]
            timestamp = unix_ms_to_date(list(latitudes.keys())[list(latitudes.values()).index(selected_lat)])

            print(index)
            print("Timestamp:", timestamp)
            print("Selected latitude:", selected_lat)
            print("Selected longtitude:", selected_lon)
            if (len(annotations)) > 0:
                annotations[-1].remove() 
            annotation = ax.annotate(str(timestamp), xy=(selected_lon, selected_lat), xycoords="data", xytext=(0.8, 0.8), textcoords='axes fraction', arrowprops=dict(facecolor='orange', color='orange', shrink=0.01, width=1), fontsize=14)
            fig.canvas.draw()
            annotations.append(annotation)

        ax.scatter(pts_x, pts_y, transform=proj, s=3, c='darkblue', picker=True)
        fig.canvas.mpl_connect('pick_event', onpick)

        plt.show()

    except getopt.GetoptError:
        print("Could not parse file. Please specify file with -f or --file=")
        sys.exit(2)

if __name__ == "__main__":
   main(sys.argv[1:])