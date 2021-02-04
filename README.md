# google-tracking-viz
## A visualization script written in Python for parsing your location history provided by our overlords at Google.

To run the script, create a Google Takeout containing your location history [https://takeout.google.com/](here).
Then install the requirements needed with `python -m pip install -r requirements.txt`. You can do this in a `venv` if you want, but matplotlib will most likely complain about not being able to show the figure.
When the setup is done, simply run `python tracking-viz.py -f [PATH-TO-FILE]` and the map will show up.
There is much more data in the JSON file than what is plotted, so feel free to contribute improvements.