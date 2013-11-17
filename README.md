THIS_GIT_REPO_NAME

SET-UP
-------
0. Fork this repo and pull to local dir
    * git clone 
    * cd THIS_GIT_REPO_NAME
1. Create/rename repo and heroku app
    * pip install cherrypy
    * pip install Twython
    * heroku create --stack cedar
    * heroku apps:rename YOUR_APP_NAME

2. Create a new twitter account at https://twitter.com/
    * Suppose your handle is @newtwitter, and your personal email is myemail@gmail.com.
        - Then for your email associated with the account, use myemail+newtwitter@gmail.com.
    (* Update your profile name, description, and background.)
    (* Follow a lot of popular twitter accounts and you will be rewarded with auto-follows by other bots.)
3. Check your email and confirm the email address for your new twitter account.
4. Create a new app at https://dev.twitter.com/apps
    * Go to Settings and find the "Application Type" heading
        - Enable "Read and Write"
        - Check "Allow this application to be used to Sign in with Twitter"
5. Setup environment variables # https://devcenter.heroku.com/articles/config-vars
    * locally: update '.env' with twitter app keys
    * heroku (uses variables in .env)
        - heroku plugins:install git://github.com/ddollar/heroku-config.git
        - heroku config:push
        (NOTE: to update, run 'heroku config:push --overwrite')
        (NOTE: to add heroku environment variable not in '.env', run 'heroku config:set YOUR_ENV_VAR=replace_this')

6. Adjust the variable 'message' in model.py line 21
    * To run locally, run 'foreman start' and open 0.0.0.0:5000 in a browser
        - This should make your bot tweet.
7. Push changes to heroku
    * Run 'heroku open' to visit your herokuapp's url
        - This should make your bot tweet.
8. Set up cron job calling your YOUR_APP_NAME.herokuapp.com at easycron.com every hour or so # http://www.easycron.com/user
    * You will have to renew your account once a month to keep it free
