# i-Content
### Video Demo: https://youtu.be/_U3FQ0qScfs

### Description: The project uses the Flask framework, CSS, HTML, SQLite3, Bootstrap, and DB Browser for SQLite This is a hub for a user where they can personalize their own page full of interesting content based on their search queries.


1. Flask framework
2. CSS
3. HTML
4. SQLite3
5. Bootstrap
6. DB Browser for SQLite

### This is a hub for a user where they can personalize their own page full of interesting content based on their search queries

There are HTML pages for:

* a user's content home page
* an about page to explain the purpose of the web application
* an error page rendering a customized error message if something goes awry
* a login page
* a register user page
* a page showing index of past generated content
* a general layout template from which all the other templates inherit their properties

 #### A portion of this code was refactored from Problem Set 9: Finance from CS50's class, including the layout HTML page, the login route and the logout route, the hashed_password functions from Werkzeug's libraries, and some bootstrap dependencies. I also adamantly refrained from availing the CS50 codespace and it was taxing figuring out how to configure database and API keys locally, but I did it, by golly.

 ### to configure the database, I searched stack overflow *ad nauseum*. I also googled elsewhere, and as the comments in the files say, there were online tutorials which assisted me in the configuring of the database programmatically, as well as configuring a config.py file using python, so that my API key for the Youtube API would not have to be hardcoded. In the real world, that would be a major security issue.

 #### In addition, I got a stock favicon from a website and embedded it into my layout,html to have a custom favicon in the user's browser. The cloud bubble reflects the whole "reflection of life's content" idea.

 #### For the html templates used: in summary, I based them off of one super class template. The various templates display the register and login pages, the "about-the-developer" page, as well as the *content* page, the most importat piece of the puzzle. ***This page pulls in the api from Youtube Data API in Google Developer, and the app.py file parses the json response such that it will give the user the top hit of the unique video id.*** 
 
 #### The content.html page uses this code: `<iframe src="https://www.youtube.com/embed/{{ video_name }}" `

 #### which allows the user to pull in only the video id and place via jinja into that src attribute in the code. Thus, the page will play any video according to your search query. Then, a user can write their thoughts in the textarea box below the video, either simulataneously or after watching.

### The Youtube Data API was used through my google developer account. URL to the Youtube Data API: https://developers.google.com/youtube/v3/

***This is my final project for Harvard's CS50: Intro to Computer Science, taught by David Malan. Special thanks to Mr. Malan, Doug Lloyd, Bryan Yu, and all else on staff. I started this MOOC three years ago, from the beginning of the COVID-19 pandemic until now. I worked on it off and on, and restarted it in 2022. Needless to say, it was hard, but very rewarding indeed. Rock on, you Ivy League superstars, you. `:) :)`***
