A social media graphQl API, built using fastApi framework

## Features
- get, add, remove and update posts.
- get, add, remove and update users.
- get, add, remove and update comments.
- get, add and remove likes.
- get, add and remove follows.
- ...



|            | Add | Update | Remove | get one  | get all |
|------------|-----|--------|--------|----------|---------| 
| posts      | [x] |  [x]   |  [x]   |    [x]   |   [x]   |
| users      | [x] |  [x]   |  [x]   |    [x]   |   [x]   |
| comments   | [x] |  [x]   |  [x]   |    [x]   |   [x]   |


|            | toggle | get one | get all|
|------------|--------|---------|--------|
| likes      |  [x]   |   [x]   |  [x]   |
| follows    |  [x]   |   [x]   |  [x]   |


## Queries and mutations

### User
- fields:
    - id
    - username
    - email
    - password
    - bio
    - avatar_url
    - created_at
    - posts
    - posts_count
    - followers
    - following
    - followers_count
    - following_count 
    - is_followed
- queries: 
    - me()
    - all_users(limit, offset)
    - one_user(id)
    - search_users(query)
- mutations:
    - create_user(username, email, password)
    - delete_user(id)
    - update_user(id, avatar_url, username, email, bio)
    - login(username, password)


### Post
- fields:
    - id
    - content
    - attachement
    - created_at
    - updated_at
    - author
    - comments
    - likes
    - comments_count
    - likes_count
    - is_liked
- queries: 
    - all_posts(limit, offset)
    - one_post(id)
- mutations:
    - create_post(content, attachement)
    - delete_post(id)
    - update_post(id, content, attachement)


### Comment
- fields:
    - id
    - content
    - created_at
    - updated_at
    - author
    - post
- queries: 
    - all_comments(limit, offset)
    - one_comment(id)
    - comment_by_post(post_id)
- mutations:
    - create_comment(post_id, content)
    - delete_comment(id)
    - update_comment(id, content)


### Like
- fields:
    - user_id
    - post_id
    - author
- queries: 
    - all_likes(limit, offset)
    - like_by_post(post_id)
    - like_by_user(user_id)
- mutations:
    - toggle_like(post_id)


### Follow
- fields:
    - follower_id
    - followed_id
    - follower
    - followed
- queries: 
    - all_follows(limit, offset)
- mutations:
    - toggle_follow(user_id)





## Tables

| users table |     | posts table |      | comments table |
|-------------|     |-------------|      |----------------|
| id          |     | id          |      | id             |
| username    |     | content     |      | content        |
| email       |     | attachement |      | author_id      |
| password    |     | author_id   |      | author         |
| bio         |     | author      |      | post_id        |
| avatar_url  |     | comments    |      | post           |
| created_at  |     | likes       |      | created_at     |
| posts       |     | created_at  |      | updated_at     |
| followers   |     | updated_at  |      
| following   |                           



| comments table |     | comments table |
|----------------|     |----------------|
| follower_id    |     | post_id        |
| followed_id    |     | user_id        |
| follower       |     | author         |
| followed       |

