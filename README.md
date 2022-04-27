# sour-scouse

```
heroku create sour-scouse
heroku buildpacks:set heroku/python
git add *
git commit -m "message"
git push heroku refactor/chalice:main
heroku ps:scale web=1
```
