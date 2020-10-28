# [Big Data Bowl 2021](https://www.kaggle.com/c/nfl-big-data-bowl-2021/overview)

## Competition Description (from Kaggle)

When a quarterback takes a snap and drops back to pass, what happens next may seem like chaos. As offensive players move in various patterns, the defense works together to prevent successful pass completions and then to quickly tackle receivers that do catch the ball. In this year’s Kaggle competition, your goal is to use data science to better understand the schemes and players that make for a successful defense against passing plays.

In American football, there are a plethora of defensive strategies and outcomes. The National Football League (NFL) has used previous Kaggle competitions to focus on offensive plays, but as the old proverb goes, “defense wins championships.” Though metrics for analyzing quarterbacks, running backs, and wide receivers are consistently a part of public discourse, techniques for analyzing the defensive part of the game trail and lag behind. Identifying player, team, or strategic advantages on the defensive side of the ball would be a significant breakthrough for the game.

This competition uses NFL’s Next Gen Stats data, which includes the position and speed of every player on the field during each play. You’ll employ player tracking data for all drop-back pass plays from the 2018 regular season. The goal of submissions is to identify unique and impactful approaches to measure defensive performance on these plays. There are several different directions for participants to ‘tackle’ (ha)—which may require levels of football savvy, data aptitude, and creativity. As examples:

- What are coverage schemes (man, zone, etc) that the defense employs? What coverage options tend to be better performing?

- Which players are the best at closely tracking receivers as they try to get open?

- Which players are the best at closing on receivers when the ball is in the air?

- Which players are the best at defending pass plays when the ball arrives?

- Is there any way to use player tracking data to predict whether or not certain penalties – for example, defensive pass interference – will be called?

- Who are the NFL’s best players against the pass?

- How does a defense react to certain types of offensive plays?

- Is there anything about a player – for example, their height, weight, experience, speed, or position – that can be used to predict their performance on defense?

What does data tell us about defending the pass play? You are about to find out.

**Note**: Are you a university participant? Students have the option to participate in a college-only Competition, where you’ll work on the identical themes above. Students can opt-in for either the Open or College Competitions, but not both.

## Directory Purpose

This directory houses the code to load, transform, plot, and analyze the data provided for the competition. It follows the following layout:

## Directory Layout
```
big_data_bowl
├── bdb_helpers/                
│   ├── coord_ops.py            # Functions to manipulate and transform coordinates
│   ├── data_loaders.py         # Functions to load the datasets
│   ├── data_mergers.py         # Functions to merge datasets together
│   ├── file_movers.py          # Functions to manipulate files in the file system
│   ├── input_checkers.py       # Functions to check the inputs to other functions to ensure validity
│   ├── lookup.py               # Functions to help find and search for different instances in the datasets
│   ├── make_test_plots.py      # Functions to test the plotting capabilities in plot_helpers.py
│   ├── plot_helpers.py         # Functions to make plots for the analyses
│   ├── scrape_team_logos.py    # Scrape logos from ESPN's website
├── img/
│   ├── logos/                  # Folder with logos for all teams, the NFL, the NFC, and AFC
│   ├── test_plots/             # Folder with demo plots to show what team colors look like once plotted
├── .gitignore                  # Files to ignore when commiting to git repository
├── bdb_filepaths.py            # Filepath centralization
├── requirements.txt            # Required packages and versions for this repository
└── README.md                   # README for Directory
```

## Author
<a href="mailto:ross.a.drucker@gmail.com">Ross Drucker</a>
