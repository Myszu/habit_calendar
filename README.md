# Habits Calendar
A calendar that specifically helps to track repetitive tasks and make habits of them.
I am creating it with a focus of my needs but with others in mind. I will try my best to make it modular, easy to read and adjust.

In my case this will be displayed on old Windows Tablet not even connected to any network (hence choice of SQLite as local storage + it is fairly easy to switch for e.g. MySQL), but hanged on a wall so I can simply check progress and condition of my habits.

## To Do
- [x] ~~Add user page~~ ver. 1.0.5 (09/17/23)
- [ ] Allow to add users (mainly because I sometimes need to check how often my son does, or does not do something 😅)
- [x] ~~Allow user to add habits~~ ver. 1.0.12 (09/23/23)
- [x] ~~Add frequency and period for measuring the habit progres (how often do you want to perform it and for how many days)~~ ver. 1.0.13 (09/24/23)
- [ ] Decide how to display tasks (buttons on a calendar or separate frame)

## Weekend Skip
I think that at first the function of active and passive might be hard to understand (even I got it confused in the initial explaination). Frankly - in some cases there will be no difference at all - for example if you want the task to occur every single day. The difference is more visible the wider is the spread between tasks. For example if you want the task to show every other day for 7 days since 01.09.2023, then the ouutput will be:

Active
    01.09.2023, 04.09.2023, 05.09.2023, 07.09.2023, 11.09.2023, 13.09.2023, 15.09.2023

Passive
    01.09.2023, 05.09.2023, 07.09.2023, 11.09.2023, 13.09.2023, 15.09.2023, 19.09.2023

So in simple words active i passing all weekend like it never happened and continues right after. Passive on the other hand is counting the weekend, but not placing the tasks. As I said, the difference becomes even more obvious, when we plan the task every three days:

Active
    01.09.2023, 04.09.2023, 07.09.2023, 11.09.2023, 13.09.2023, 18.09.2023, 19.09.2023

Passive
    01.09.2023, 04.09.2023, 07.09.2023, 13.09.2023, 19.09.2023, 22.09.2023, 25.09.2023

Hope this helps :)
