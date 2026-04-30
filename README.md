# Tempo
Running Log and Planner
___________
## About


Tempo is designed to be a modular running log that doesn't restrict you to the typical weekly
structure.  You are able to create your own 'cycles', whether that means the usual 7-day cycle or
anything greater or less than that, it's up to you to decide on a cycle by cycle basis.
---
## Built With
Django - Backend Framework

PostgreSQL - Database

Vanilla JS - Dynamic UI Interactions

Upsun (Platform.sh) - Deployment

---
## Getting Started

### Web Version: 
https://main-bvxea6i-4me5w5cerszyu.us-4.platformsh.site/

### Installing Locally:
#### Prerequisites

Before installing the Python dependencies, ensure you have the following installed on your system:

- Python 3.14+

- PostgreSQL 14+

- A Database User: Create a user with permissions to create databases.

#### Database Setup
Create a local database for the project:

```
createdb run_tracker_db
```
Set up your environment variables (or .env file) with your database credentials:
```
DB_NAME=run_tracker_db
DB_USER=your_username
DB_PASSWORD=your_password
```
#### App Setup
```
# Clone the repository
git clone https://github.com/muno17/Tempo.git
cd Tempo

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations and start the server
python manage.py migrate
python manage.py runserver
```
---
## Usage

1. **Sign Up for an account or Log In if you already have one**.  By default, there is a demo account set up
so that if you don't log in, you can still utilize the app and test out any of its functionality. 
However, anyone who isn't logged in will be able to see all entries that have been added to the demo account.


2. **Create a Shoe** so that you have gear to track.  Adding shoes is optional, but it is helpful to create a shoe first
before adding activities if you desire to track your gear.  You will be able to add shoes later on and
edit activities to associate them.


3. **Create a Block** to set up your custom macrocycle.  Blocks house cycles and are meant to be a high
level overview of your current phase in training.  For example, if you are training for a specific 5k
race you can set up a block that begins on the date you intend to start your focused 5k phase and ends
the day of your goal race.  Blocks allow you to track total mileage and pace which is useful for comparing
to past and future blocks.


4. **Create a Cycle** to set up your custom microcycle.  Cycles are your 'week' and can be set up to last
any amount of days by selecting any start and end date that you choose.  Cycles can be varying lengths
of time so you don't have to feel constrained by the usual 7-day weekly cycle.  Cycles are used to house
activities, and like blocks give you useful stats to compare cycle to cycle.


5. **Create an Activity** to add a specific run.  Within activities, you can add segments (up to 10 currently)
where each segment can be a different part of a run/workout.  For example, if your activity
for the day was a 30 minute easy run, you would just use one segment.  If your running workout
was something like a set of 5 intervals, you could use one segment per interval.

Once you have created one of each level of entry, you can view them by clicking on the respective
link to be directed to a tabular view of all logged versions of that entry.  If you click on the 
row that is displaying an entry, it will take you to its details where it will also include any of its
children entries (if any have been associated).

At any point while viewing entries, you can click on the 'use km' checkbox to convert all units
from mile to kilometers.  If the checkbox is selected, you can also create activities/segments
using kilometers instead of miles.  As of this writing, clicking on the toggle while
viewing a creation form will not toggle between units, so make sure that the checkbox is 
toggled on before creating an activity if you intend to enter in information in kilometers.
***Please note that all distances are stored in miles within the database even if they were 
entered in as kilometers.  This may lead to slight rounding errors due to float precision when viewing entries.
For example, if you create a 10km activity, it will display as 9.99km***

Editing any entry is simple and can be achieved by clicking on the corresponding 'Update'
button either in the entry's row or from within its details.  This will bring up the same
form as when you created the entry, only that the fields will already be filled out with
the current values.

Deleting an entry can be achieved by clicking on the corresponding 'Delete' button either in the
entry's row or from within its details.  This will navigate you to a page to confirm deletion.




