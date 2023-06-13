# anime-recommender-bot
- Bot telegram nickname: @anime_recommender_bot
- Link: https://t.me/anime_recommender_bot
---
I dont plan to deploy it any time soon. So if it doesn't reply to you, it's just not running.

For bug report and stuff you can message me in telegram, my username: @Koganovskiy

September, 2020

### How it works
Any anime has few parameters that can be used to give recommendations.
This particular system uses 6 parameters:
- rating
- genres
- views
- release date
- number of episodes
- duration of one episode 

Of course, various parameters have different value for different people. So if we want to get recommendation score for each anime title and our equation looks like this:
##### rating * a + genres * b + views * c + ... + duration * f = recommendation_score
All six factors (a, b, c ... f) should be different for diffenrent users, but how to calculate them? 
System harvests parameters for titles that user have rated and bruteforces all factors with simple genetic algorithm so result of output formula would be as close to user's ratings as possible.
When system calculated final formula for specific user it can simply get recommendation score for all titles in database and give user ones with highest recommendation score.

### Technologies
- SQLite databse for anime meta data and users data
- pyTelegramBotAPI library for communication with telegram API

### Source
All anime data was parsed from <b>myanimelist.net</b>. <i><strike>please, dont sue me</strike></i> Thank them very much!

##### Special thanks to:
<i>@syasinaeg
@a_rahmanovsky</i>

G.Koganovskiy 2020
