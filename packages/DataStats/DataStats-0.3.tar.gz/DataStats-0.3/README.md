# Data_Stats
## A package to make easier the obtention of data from the database _"statsbombpy"_

[![STATSBOMB](https://miro.medium.com/max/2970/0*fIjnUoscUWWWR-nB.png)](https://statsbomb.com/es/)

Data_Stats is a library that makes your life easier when you want to get data from the open [source](https://github.com/statsbomb/statsbombpy), helping you to get organized data instead of pulling the data in a unique way from game to game so you can pull an entire season for example.

## Instalation
To install this library the easiest way to do it is via PyPi:
```
pip install DataStats
```

## Source code
You can check the latest sources with the command:
```
git clone https://github.com/pauloo1010/Paulo-Inigo-Progra.git
```

## Files
-> Data_Stats folder
> Data_Stats.py: Code of all the library that will  be explained in the Features section
> __ init__.py: Import of the library

-> LICENSE.txt: Copyright license
-> setup.cfg: Description file
-> setup .py: This file contains information about the package that PyPi needs

## Features

In this library, three different functions have been used within the created class:
1. The function **_selection_** returns a df with needed information for the other two functions as competition_id or season_id. 

2. The function **_matches_** returns another df that contains every match from the season that you have specified before, this process is made possible by the innformation that selection has provided. 

3. The last funtion **_events_** returns a list with two different dictionaries inside. 
In the first dictionary the keys are the ids of the match_id and the information inside each key is a dictionary with the information of all the existing tables of that match.
The keys of the second dictionary are the names of the tables and inside them are joined all the data from all the matches.

## Example
Importing library
```sh
from DataStats import StatsObtention  
```
In the following command within the brackets you can enter different values. In case you enter a wrong one, this library will help you by telling the possible values you have for each case.

![image](https://raw.githubusercontent.com/pauloo1010/Ejercicio_github/master/wrong%20data.jpeg)

```sh
a = StatsObtention('La Liga', 'male', '2009/2010')
```
To know the usefulness of the commands that are going to be presented in the following boxes, you can refer to the information in the section of _"Features"_.
```
a.selection()
```
![image](https://raw.githubusercontent.com/pauloo1010/Ejercicio_github/master/1linea.jpeg)
```
a.matches()
```
![image](https://raw.githubusercontent.com/pauloo1010/Ejercicio_github/master/tabla.jpeg)

This command has two processes that are carried out as shown in the following screenshots, the first one consists of creating the first dictionary that has been discussed in the _"Features"_ section and the second one consists of creating the second dictionary that is also explained in the same section as the previous one.
```
a.events()
```

![image](https://raw.githubusercontent.com/pauloo1010/Ejercicio_github/master/porcenta.jpeg)

![image](https://raw.githubusercontent.com/pauloo1010/Ejercicio_github/master/creating%20table.jpeg)

![image](https://raw.githubusercontent.com/pauloo1010/Ejercicio_github/master/process.jpeg)
