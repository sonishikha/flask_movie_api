# movie_store

# API list
- get_movie_details - singular movie details. based on id.
- get_movie_list - filters- name . relase : 2023. 
- get_comments - n number of comments based on movie id.
- get_favorites
- add_favorites - _id
- remove_favorites - _id

-------------
- get_genre - will query all the distinct genres and provide result accordingly.
- get_languages

comments
add - 
get
delete

------------------
listing - name,release time,imdb rating, number of comments,poster.

comments collection
movie_id : foreign key to id in movies db
comments : {
    id: 1, comment: "some text", like : 1, dislike: 1, username: test, datetime: date time
    id: 2, comment: "some text", like : 1, dislike: 1, username: test, datetime: date time
}
