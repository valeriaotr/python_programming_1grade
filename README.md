# python_programming_1grade
In this repository there are a few laboratory works on Python, that have been done during 1st year of education in ITMO university.

## Directory descriptions
### Calculator
That's a base algorithm for calculating math operations through the console line.

Available operations:
```
* Converting a number from a decimal number system to a number system with a base from 2 to 9.
* Base math operations ("+", "-", "/", "*", "**"
* Other math operations ("sin", "cos", "tg", "^2", "lg"
```

### Descriptive Data Analysis
In this laboratory work, a dataset on the peculiarities of music genres was analyzed, containing 41700 unique performers.

Completed Tasks:

Task #1:
```
Print the percentage of each genre in the dataset.
Show the distribution of the number of tracks by genre on a horizontal bar chart. Highlight the genre with the most songs in contrasting color.
Find the most popular dance genre. For the dance genre itself, the average value of the danceability indicator should be the highest.
For each genre, determine which key prevails in it – the number of tracks of which key is greater (minor or major).
```

Task #2:
```
Output the artist who has the most tracks in the dataset. And the one with the least of them.
Show the top 20 performers on a horizontal bar chart. Study the result and draw conclusions.
```

Task #3:
```
Build a correlation matrix for the characteristics of the tracks. Which characteristics are strongly correlated? Which ones are weak? Are there characteristics between which there is practically no correlation?
Calculate the correlation between popularity and the length of the track name.
```

Task #4:
```
Show the ratio of track popularity to genre on the box diagram. What genres are similar to each other?
```

Task #5:
```
For the top 3 genres, show the pie chart with the grouping of the most popular artist. There should be one diagram.
```

Task #6:
```
On the vertical bar chart for the most popular and most unpopular genres, show the average values for all characteristics. Show the negative and positive values of the characteristics in different colors.
```

Task #7:
```
Add a categorical track length column to the data, which will contain the values: "short" (<=3 min), "medium" (>3min, <=5min), "long" (>5min).
Show a graph of the density distribution of the data in the loudness column, grouped by duration categories.
On a pie chart of the "donut" type, show the numerical ratio of tracks of different durations.
```

Task #8 (SQL):
```
Complete some tasks using SQL
```
### Hackernews
In this laboratory work it was needed to build a native ML model using Bayes (the goal of the model is to give the user the opportunity to classify news using marks like "negative", "neutral", "positive")


To find the news to clasify we've created a parser for the website https://news.ycombinator.com/


All the news were located in DataBase (the engine was used using a function from the sqlalchemy module, the engine is a database engine that manages connection and interaction with the database. In this case, the SQLite engine is used, and the database will be stored in the news.db file (if the file does not exist, it will be created).)


### Maze

Algoithm for solving maze-puzzles

### RSA, Vigenere, caesar

In this laboratory works were realized three different encryption algorithms: RSA, vigenere, caesar

### Tg bot

In this laboratory work was realized a Telegram-Bot for easily adding deadlines to the table in Google-Sheets.

Telegram-Bot has following functions:
```
* Validate a date for a deadline
* Validate a link to a subject
* Connect to a Google-Sheets table
* Edit subjects in a table
* Edit deadlines in a table
* Check deadlines for a current week
* Delete subject
* Delete deadline
* Update deadline for a subject
* Edit info about a subject
```

### VK API

In this laboratory work was used a VK API to get and aggregate info about users.

Following functions are available:
```
* Predict user's age according to the ages of their friends
* Build a self-centered graph of friends. The graph is visualized with the selection of node groups.
* Get list of IDs of friends of particular user by ID
* Get mutual friends of users
```
